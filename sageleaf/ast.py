from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Prog:
    stmnts: list[Stmnt]


@dataclass
class Imp:
    path: Idf


@dataclass
class Def:
    idf: str
    expr: Expr


@dataclass
class Appl:
    expr1: Expr
    expr2: Expr


@dataclass
class Map:
    pairs: list[tuple[Expr, Expr]]


@dataclass
class Str:
    string: str


@dataclass
class Num:
    number: float


Idf = str

Expr = Appl | Map | Str | Num | Idf

Stmnt = Imp | Def | Expr
