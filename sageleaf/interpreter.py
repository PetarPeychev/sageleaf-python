import os
from pathlib import Path
from copy import deepcopy

from sageleaf import ast
from sageleaf.syntax import Lexer
from sageleaf.semantics import Parser


class RuntimeException(Exception):
    """Error raised during runtime execution."""


class Interpreter:
    def __init__(self):
        self._env = {}

    def _throw(msg: str):
        print(f"Exception: {msg}")

    def program(self, p: ast.Prog):
        for s in p.s:
            self.statement(s)

    def statement(self, s: ast.Stmnt):
        if isinstance(s, ast.Req):
            self.require(s.p)
        elif isinstance(s, ast.Def):
            self._env[s.idf] = s.e

    def require(self, p: str):
        if p.startswith("sage."):
            path = os.path.dirname(__file__) + \
                "/builtins/" + p.removeprefix("sage.")
        elif os.path.isfile(p):
            path = p
        else:
            raise RuntimeException(f"Invalid module path {p}.")
        path += ".sage"
        code = Path(path).read_text()
        tokens = Lexer(code).lex()
        prog = Parser(tokens).parse()
        self.program(prog)

    def run_main(self):
        print(self.expression(self._env["main"], deepcopy(self._env)))

# Appl | Let | Map | Str | Num | Bool | Idf
    @staticmethod
    def expression(expr: ast.Expr, env: dict[str, ast.Expr]):
        if isinstance(expr, ast.Bool):
            pass
