import sys
from operator import index
from types import TracebackType
from typing import (Any, Dict, Generator, Iterator, List, MutableSequence, NoReturn, Optional, SupportsIndex, Type,
                    Union, overload)
from typing_extensions import Literal

from kola.exception import KoiLangError
from kola.lexer import BaseLexer, StringLexer
from kola.parser import Parser
from kola.klvm import Command, CommandSet, Environment, KoiLang, kola_command
from kola.lib.recorder import Instruction, recorder


class CodeSection:
    __slots__ = ["_codes", "base", "_length"]

    def __init__(self, __base_codes: Union[List[Instruction], "CodeSection", None] = None, base: int = 0) -> None:
        self._length = -1
        self.base = 0
        if __base_codes is None:
            # run in real address mode
            assert base == 0
            self._codes = []
        elif isinstance(__base_codes, list):
            assert base == 0
            self._codes = __base_codes
            self._length = len(__base_codes)
        else:
            self._codes = __base_codes._codes
            self.base = base + __base_codes.base
    
    def __getitem__(self, __index: SupportsIndex) -> Instruction:
        __index = index(__index)
        if __index < 0 or (self._length >= 0 and __index >= self._length):  # pragma: no cover
            raise JKlvmAddressError("instruction access out of bounds", address=__index)
        __index += self.base
        return self._codes[__index]
    
    def append(self, instruction: Instruction) -> None:
        if self._length != -1:
            raise RuntimeError("modify a frozen section")
        self._codes.append(instruction)
    
    def freeze(self, end: int = 0) -> None:
        if self._length <= 0:
            self._length = end or len(self._codes)
    
    def __iter__(self) -> Iterator[Instruction]:
        return iter(self._codes[self.base:self.base + len(self)])
    
    def __bool__(self) -> bool:
        return self._length > 0 or bool(self._codes)
    
    def __len__(self) -> int:
        if self._length >= 0:
            return self._length
        raise RuntimeError("The effective length of this environment section is not set")  # pragma: no cover


class JCommandSet(CommandSet):
    """
    base class for JKLvm classes
    """
    codes: CodeSection
    labels: Dict[str, int]
    exit_points: Dict[int, int]

    def __init__(self) -> None:
        super().__init__()
        self.__ip = 0
        self.labels = {}
        
    def step(self) -> Any:
        name, args, kwargs = self.codes[self.ip]
        self.__ip += 1
        try:
            return self[name](*args, **kwargs)
        except KoiLangError:
            if not self.on_exception(*sys.exc_info()):
                raise
    
    def add_label(self, name: str, address: int) -> None:
        self.labels[name] = address
    
    def goto(self, __address: Union[int, str]) -> NoReturn:
        if isinstance(__address, str):
            __address = self.labels[__address]
        raise JKLvmJump(__address, base=self.codes.base)
    
    def exit(self) -> NoReturn:
        raise JKLvmExit(0)
    
    @property
    def ip(self) -> int:
        return self.__ip
    
    @ip.setter
    def ip(self, __address: int) -> None:
        if __address < 0 or __address >= len(self.codes):  # pragma: no cover
            raise JKlvmAddressError("instruction access out of bounds", address=__address)
        self.__ip = __address
    
    @kola_command("@exception", virtual=True)
    def on_exception(self, exc_type: Type[KoiLangError], exc_ins: Optional[KoiLangError], traceback: TracebackType) -> Any:
        if issubclass(exc_type, JKLvmExit):
            # set the value of the ip register to the length of
            # the code cache to make JKlvm exit the loop.
            self.__ip = len(self.codes)
            return True
        elif issubclass(exc_type, JKLvmJump):
            assert isinstance(exc_ins, JKLvmJump)
            self.ip = exc_ins.address + exc_ins.base
            return True
        return False


class JEnvironment(JCommandSet, Environment):
    """
    an environemnt implementation that can use jump instructions in the environment
    """
    __slots__ = ["codes", "state", "labels"]

    # state flag
    STATE_RECORD = -1
    STATE_READ_AHEAD = 0
    STATE_EXECUTE = 1
    STATE_INHERIT = 2

    def __read_ahead(self, base: "JKoiLang") -> None:
        if not hasattr(base, "exit_points"):
            base.exit_points = {}
        
    def __execute(self) -> None:
        self.ip = 0
        length = len(self.codes)
        while self.ip != length:
            self.step()
    
    @property
    def ip(self) -> int:
        if self.state <= JEnvironment.STATE_READ_AHEAD:  # pragma: no cover
            raise RuntimeError("cannot use reg ip in redaing mode")
        elif self.state == JEnvironment.STATE_INHERIT:
            home = self.jhome
            return home.ip - self.codes.base
        return super().ip
    
    @ip.setter
    def ip(self, __address: int) -> None:
        if self.state <= JEnvironment.STATE_READ_AHEAD:  # pragma: no cover
            raise RuntimeError("cannot use reg ip in redaing mode")
        elif self.state == JEnvironment.STATE_INHERIT:
            home = self.jhome
            home.ip = __address + self.codes.base
        else:
            super().ip = __address
    
    @property
    def jhome(self) -> JCommandSet:
        cur = self
        while isinstance(cur, Environment):
            if isinstance(cur, JEnvironment) and cur.state in [
                JEnvironment.STATE_EXECUTE, JEnvironment.STATE_READ_AHEAD,
            ]:
                return cur
            cur = cur.back
        else:
            if not isinstance(cur, JKoiLang):  # pragma: no cover
                raise TypeError("no running JKLvm found")
            return cur

    def set_up(self, cur_top: CommandSet) -> None:
        super().set_up(cur_top)

        self.labels = {}
        while isinstance(cur_top, Environment):
            if isinstance(cur_top, JEnvironment):
                if cur_top.state <= JEnvironment.STATE_READ_AHEAD:
                    self.state = JEnvironment.STATE_RECORD
                else:
                    self.state = JEnvironment.STATE_INHERIT
                break
            cur_top = cur_top.back
        else:
            if isinstance(cur_top, JKoiLang):
                self.state = JEnvironment.STATE_INHERIT
                if not hasattr(cur_top, "exit_points"):
                    cur_top.exit_points = {}
            else:
                self.state = JEnvironment.STATE_READ_AHEAD
                self.codes = CodeSection()
                self.exit_points = {}
                return
        self.codes = CodeSection(cur_top.codes, cur_top.ip - 1)
        if self.state == JEnvironment.STATE_INHERIT:
            try:
                m_ep = self.jhome.exit_points
                length = m_ep[self.codes.base]
            except Exception as e:
                raise JKlvmAddressError("fail to fetch infomation of the exit point", address=self.ip) from e
            self.codes.freeze(length)
    
    def tear_down(self, cur_top: CommandSet) -> None:
        if self.state == JEnvironment.STATE_RECORD:
            jhome = self.jhome
            assert isinstance(jhome, JEnvironment)
            jhome.exit_points[self.codes.base] = self.ip
        elif self.state == JEnvironment.STATE_READ_AHEAD:
            self.state = JEnvironment.STATE_EXECUTE
            self.__execute()
        super().tear_down(cur_top)
    
    def on_exception(self, exc_type: Type[KoiLangError], exc_ins: Optional[KoiLangError], traceback: TracebackType) -> bool:
        if issubclass(exc_type, JKLvmExit):
            assert isinstance(exc_ins, exc_type)
            if exc_ins.target is self:
                try:
                    m_ep: Any = self.jhome.exit_points  # type: ignore
                    self.ip = m_ep[self.codes.base]
                except Exception as e:
                    raise JKlvmAddressError("fail to fetch infomation of the exit point", address=self.ip) from e
                self.on_autopop()
                return True
        return self.back["@exception"](exc_type, exc_ins, traceback)

    def __kola_caller__(self, command: Command, args: tuple, kwargs: Dict[str, Any], **kwds: Any) -> Any:
        if self.state > JEnvironment.STATE_READ_AHEAD:
            return super().__kola_caller__(command, args, kwargs, **kwds)
        # preread mode, just record to cache
        assert isinstance(self.codes, MutableSequence)
        self.codes.append(Instruction(command.__name__, args, kwargs))


class JKoiLang(JCommandSet, KoiLang):
    """
    a KoiLang implementation that can use global jump instructions
    """
    __slots__ = ["codes", "labels"]

    def __execute(self) -> Generator[Any, None, None]:
        self.codes.freeze()
        with self.exec_block():
            while self.ip != len(self.codes):
                yield self.step()

    @overload
    def parse(self, lexer: Union[BaseLexer, str], *, with_ret: Literal[False] = False, close_lexer: bool = True) -> None: ...
    @overload  # noqa: E301
    def parse(
        self,
        lexer: Union[BaseLexer, str],
        *,
        with_ret: Literal[True],
        close_lexer: bool = True
    ) -> Generator[Any, None, None]: ...
    def parse(self, lexer: Union[BaseLexer, str], *, with_ret: bool = False, close_lexer: bool = True) -> Any:  # noqa: E301
        if isinstance(lexer, str):
            if not close_lexer:
                raise ValueError("inner string lexer must be closed at the end of parsing")
            lexer = StringLexer(
                lexer,
                encoding=self.__class__.__text_encoding__,
                command_threshold=self.__class__.__command_threshold__,
                no_lstrip=not self.__class__.__text_lstrip__
            )
        
        # read all command info
        codes = []
        while True:
            try:
                codes.extend(Parser(lexer, recorder))
            except KoiLangError:
                if not self.on_exception(*sys.exc_info()):
                    if close_lexer:
                        lexer.close()
                    raise
            else:
                break
        if close_lexer:
            lexer.close()
        
        # start execution
        self.codes = CodeSection(codes)
        gen = self.__execute()
        if with_ret:
            return gen
        for _ in gen:
            pass
    
    def at_start(self) -> None:
        super().at_start()
        self.ip: int = 0
        self.labels: Dict[str, int] = {}


class JKLvmException(KoiLangError):
    """the base exception used in JKLvm"""
    __slots__ = []


class JKlvmAddressError(JKLvmException):
    """incurrect instruction address"""
    __slots__ = ["address"]

    def __init__(self, *args: object, address: Optional[int] = None) -> None:
        super().__init__(*args)
        self.address = address


class JKLvmExit(JKLvmException):
    """exit from an environemnt"""
    __slots__ = ["target"]
    
    def __init__(self, *args: object, target: Optional[JCommandSet] = None) -> None:
        super().__init__(*args)
        self.target = target


class JKLvmJump(JKLvmException):
    """jump to a new address"""
    __slots__ = ["address", "base"]
    
    def __init__(self, address: int, *, base: int = 0) -> None:
        super().__init__(f"{address:08X}+{base:08X}")
        self.address = address
        self.base = base
