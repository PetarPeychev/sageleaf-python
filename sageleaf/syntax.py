from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import re


class TT(Enum):
    """Token type."""
    # whitespace
    WS = auto()

    # single-character tokens
    SEMICOLON = auto()
    COMMA = auto()
    FSLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    LCURLY = auto()
    RCURLY = auto()
    LSQUARE = auto()
    RSQUARE = auto()

    # multi-character tokens
    ARROW = auto()

    # literals
    STRING = auto()

    # keywords
    IMPORT = auto()
    DEF = auto()
    AS = auto()
    LET = auto()
    BE = auto()
    IN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    UNIT = auto()

    # identifiers including any numbers
    ID = auto()


@dataclass
class T:
    """Single token."""
    tt: TT
    lexeme: str
    line: int
    col: int

    def __eq__(self, other):
        if isinstance(other, TT):
            return self.tt == other
        elif isinstance(other, str):
            return self.value == other
        else:
            return False

    def __str__(self):
        return f"{self.tt}({self.lexeme})"

    def __repr__(self):
        return str(self)


PATTERNS = {
    r"[ \t\n]+": TT.WS,
    r";": TT.SEMICOLON,
    r",": TT.COMMA,
    r"\\": TT.FSLASH,
    r"\(": TT.LPAREN,
    r"\)": TT.RPAREN,
    r"\{": TT.LCURLY,
    r"\}": TT.RCURLY,
    r"\[": TT.LSQUARE,
    r"\]": TT.RSQUARE,

    r"->": TT.ARROW,

    r"\".*\"": TT.STRING,

    r"import": TT.IMPORT,
    r"def": TT.DEF,
    r"as": TT.AS,
    r"let": TT.LET,
    r"be": TT.BE,
    r"in": TT.IN,
    r"if": TT.IF,
    r"then": TT.THEN,
    r"else": TT.ELSE,
    r"unit": TT.UNIT,

    r"[^ \t\n;,\\\(\)\[\]\{\}\"]+": TT.ID,  # any symbol not used otherwise
}


class SyntacticError(Exception):
    """Error during syntactic analysis of sageleaf code."""


class Lexer:
    def __init__(self, code):
        self._code = code
        self._idx = 0
        self._col = 0
        self._line = 1

    def _error(self, message):
        raise SyntacticError(
            f"[line {self._line}, column {self._col}] Error: {message}")

    def _next(self):
        peek = self._peek()
        if peek is not None:
            if peek == "\n":
                self._col = 0
                self._line += 1
            self._idx += 1
            return peek

    def _peek(self):
        if self._idx < len(self._code):
            return self._code[self._idx]
        else:
            return None

    def _match(self, string):
        for pattern, tt in PATTERNS.items():
            if re.fullmatch(pattern, string):
                return T(tt, string, self._line, self._col)
        return None

    def lex(self):
        tokens = []
        while True:
            string = ""
            while self._peek() is not None:
                string += self._next()
                if self._match(string):
                    if self._peek() is not None and self._match(string + self._peek()):
                        continue
                    else:
                        tokens.append(self._match(string))
                        string = ""
            if string != "":
                self._error(f"Unrecognised token `{string}`.")
            elif self._peek() is None:
                break
        return [t for t in tokens if t != TT.WS]
