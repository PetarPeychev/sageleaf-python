from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto
import re


@dataclass
class Token:
    type: TokenType
    source_idx: int
    value: Optional[str] = None


class TokenType(Enum):
    BREAK = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    COLON = auto()
    ARROW = auto()
    LAMBDA = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    GREATER = auto()
    LESSER = auto()
    GEQUALS = auto()
    LEQUALS = auto()
    IS = auto()
    LPAREN = auto()
    RPAREN = auto()
    STARTBLOCK = auto()
    ENDBLOCK = auto()
    LET = auto()
    TYPE = auto()
    OR = auto()
    AND = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    WHERE = auto()


def lex(source: str) -> list[Token]:
    idx: int = 0
    tokens: list[Token] = []

    while idx < len(source):
        if source.startswith((" ", "\t", "\n"), idx):
            idx += 1
        elif source.startswith(";", idx):
            idx += 1
            tokens.append(Token(TokenType.BREAK, idx))
        elif source.startswith(":", idx):
            idx += 1
            tokens.append(Token(TokenType.COLON, idx))
        elif source.startswith("->", idx):
            idx += 2
            tokens.append(Token(TokenType.ARROW, idx))
        elif source.startswith("\\", idx):
            idx += 1
            tokens.append(Token(TokenType.LAMBDA, idx))
        elif source.startswith("+", idx):
            idx += 1
            tokens.append(Token(TokenType.PLUS, idx))
        elif source.startswith("-", idx):
            idx += 1
            tokens.append(Token(TokenType.MINUS, idx))
        elif source.startswith("*", idx):
            idx += 1
            tokens.append(Token(TokenType.MULTIPLY, idx))
        elif source.startswith("/", idx):
            idx += 1
            tokens.append(Token(TokenType.DIVIDE, idx))
        elif source.startswith("=", idx):
            idx += 1
            tokens.append(Token(TokenType.ASSIGN, idx))
        elif source.startswith("(", idx):
            idx += 1
            tokens.append(Token(TokenType.LPAREN, idx))
        elif source.startswith(")", idx):
            idx += 1
            tokens.append(Token(TokenType.RPAREN, idx))
        elif source.startswith("{", idx):
            idx += 1
            tokens.append(Token(TokenType.STARTBLOCK, idx))
        elif source.startswith("}", idx):
            idx += 1
            tokens.append(Token(TokenType.ENDBLOCK, idx))
        elif source.startswith(">=", idx):
            idx += 2
            tokens.append(Token(TokenType.GEQUALS, idx))
        elif source.startswith("<=", idx):
            idx += 2
            tokens.append(Token(TokenType.LEQUALS, idx))
        elif source.startswith(">", idx):
            idx += 1
            tokens.append(Token(TokenType.GREATER, idx))
        elif source.startswith("<", idx):
            idx += 1
            tokens.append(Token(TokenType.LESSER, idx))
        elif source.startswith("is", idx):
            idx += 2
            tokens.append(Token(TokenType.IS, idx))
        elif source.startswith("let", idx):
            idx += 3
            tokens.append(Token(TokenType.LET, idx))
        elif source.startswith("type", idx):
            idx += 4
            tokens.append(Token(TokenType.TYPE, idx))
        elif source.startswith("or", idx):
            idx += 2
            tokens.append(Token(TokenType.OR, idx))
        elif source.startswith("and", idx):
            idx += 3
            tokens.append(Token(TokenType.AND, idx))
        elif source.startswith("if", idx):
            idx += 2
            tokens.append(Token(TokenType.IF, idx))
        elif source.startswith("then", idx):
            idx += 4
            tokens.append(Token(TokenType.THEN, idx))
        elif source.startswith("else", idx):
            idx += 4
            tokens.append(Token(TokenType.ELSE, idx))
        elif source.startswith("where", idx):
            idx += 5
            tokens.append(Token(TokenType.WHERE, idx))
        elif re.match(r"[.\d]", source[idx]):
            idx, number = lex_number(idx, source)
            tokens.append(number)
        elif re.match(r"[a-zA-Z]", source[idx]):
            idx, identifier = lex_identifier(idx, source)
            tokens.append(identifier)
        else:
            raise Exception(f"Unrecognised character: {source[idx]}")

    return tokens


def lex_number(idx: int, source: str) -> tuple[int, Token]:
    digits: list[str] = []

    while idx < len(source):
        if re.match(r"[.\d]", source[idx]):
            digits.append(source[idx])
            idx += 1
        else:
            break

    return idx, Token(TokenType.NUMBER, idx, "".join(digits))


def lex_identifier(idx: int, source: str) -> tuple[int, Token]:
    letters: list[str] = []

    while idx < len(source):
        if re.match(r"[a-zA-Z0-9_]", source[idx]):
            letters.append(source[idx])
            idx += 1
        else:
            break

    identifier = "".join(letters)

    return idx, Token(TokenType.IDENTIFIER, idx, identifier)
