from __future__ import annotations

from sageleaf.syntax import T, TT
from sageleaf import ast
import functools


class SemanticError(Exception):
    """Error during semantic analysis of sageleaf code."""


class Parser:
    def __init__(self, ts):
        self._ts = ts
        self._idx = 0

    def _error(self, message):
        raise SemanticError(
            f"[token {self._ts[self._idx]}] Error: {message}")

    def _at_end(self):
        return self._idx >= len(self._ts)

    def _match(self, *tts):
        if self._check(tts):
            self._advance()
            return True
        return False

    def _match_or_error(self, *tts, msg):
        for tt in tts:
            if self._check(tt):
                self._advance()
                return self._previous()
        self._error(msg)

    def _check(self, *tts):
        for tt in tts:
            if self._peek().tt == tt:
                return True
        return False

    def _advance(self):
        if not self._at_end():
            self._idx += 1
            return self._previous()
        else:
            return None

    def _peek(self):
        if not self._at_end():
            return self._ts[self._idx]
        else:
            return None

    def _previous(self):
        if self._idx > 0:
            return self._ts[self._idx - 1]
        else:
            return None

    def parse(self):
        stmnts = []
        while not self._at_end():
            stmnts.append(self.p_stmnt())
            self._match_or_error(
                TT.SEMICOLON, msg="Expected semicolon at end of statement.")
        return ast.Prog(stmnts)

    def p_stmnt(self):
        if self._check(TT.IMPORT):
            return self.p_import()
        elif self._check(TT.DEF):
            return self.p_def()
        else:
            self._error("Unrecognised start of statement.")

    def p_import(self):
        self._advance()
        idf = self._match_or_error(
            TT.ID, msg="Expected module identifier in import statement.")
        return ast.Imp(idf)

    def p_def(self):
        self._advance()
        idf = self._match_or_error(
            TT.ID, msg="Expected identifier in def statement.")
        self._match_or_error(TT.AS, msg="Expected 'as' in def statement.")
        expr = self.p_expr()
        return ast.Def(idf.lexeme, expr)

    def p_expr(self):
        exprs = []
        while self._check(TT.LPAREN, TT.LET, TT.LCURLY, TT.STRING, TT.ID):
            expr = None
            if self._check(TT.LPAREN):
                self._advance()
                expr = self.p_expr()
                self._match_or_error(
                    TT.RPAREN, msg="Expected end of parentheses in expression.")
            elif self._check(TT.LET):
                self._advance()
                idf = self._match_or_error(TT.ID, msg="")
                self._match_or_error(TT.BE, msg="")
                subexpr1 = self.p_expr()
                self._match_or_error(TT.IN, msg="")
                subexpr2 = self.p_expr()
                expr = ast.Let(idf, subexpr1, subexpr2)
            elif self._check(TT.LCURLY):
                expr = self.p_map()
            elif self._check(TT.STRING):
                string = self._advance().lexeme[1:-1]
                expr = ast.Str(string)
            elif self._check(TT.ID):
                idf = self._advance().lexeme
                if self.p_num(idf):
                    expr = self.p_num(idf)
                else:
                    expr = idf
            exprs.append(expr)

        if len(exprs) == 0:
            self._error("Unrecognised start of expression.")
        elif len(exprs) == 1:
            return exprs[0]
        else:
            appl = functools.reduce(lambda e1, e2: ast.Appl(e1, e2), exprs)
            return appl

    def p_num(self, idf):
        try:
            return float(idf)
        except:
            return None

    def p_map(self):
        raise NotImplementedError()
