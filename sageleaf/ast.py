from __future__ import annotations
from dataclasses import dataclass
from types import NoneType


@dataclass
class Prog:
    s: list[Stmnt]


@dataclass
class Req:
    p: Idf


@dataclass
class Def:
    idf: str
    e: Expr


@dataclass
class Appl:
    e1: Expr
    e2: Expr


@dataclass
class Map:
    p: list[tuple[Expr | Wildcard, Expr]]


@dataclass
class Wildcard:
    idf: str
    e: Expr | NoneType


@dataclass
class Let:
    idf: str
    e1: Expr
    e2: Expr


@dataclass
class Str:
    s: str


@dataclass
class Num:
    n: float


@dataclass
class Bool:
    b: bool


Idf = str

Expr = Appl | Let | Map | Str | Num | Bool | Idf

Stmnt = Req | Def
