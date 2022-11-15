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
        if self._check(TT.REQUIRE):
            return self.p_require()
        elif self._check(TT.DEF):
            return self.p_def()
        else:
            self._error("Unrecognised start of statement.")

    def p_require(self):
        self._advance()
        idf = self._match_or_error(
            TT.STRING, msg="Expected module in require statement.")
        return ast.Req(idf.lexeme[1:-1])

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
                if self.p_num(idf) is not None:
                    expr = self.p_num(idf)
                elif idf == "True":
                    expr = ast.Bool(True)
                elif idf == "False":
                    expr = ast.Bool(False)
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
        self._match_or_error(
            TT.LCURLY, msg="Expected left curly bracket in start of map.")
        elements = []
        if not self._check(TT.RCURLY):
            elements.append(self.p_arrow())
            while self._check(TT.COMMA):
                self._advance()
                elements.append(self.p_arrow())
        self._match_or_error(
            TT.RCURLY, msg="Expected right curly bracket in end of map.")
        return ast.Map(elements)

    def p_arrow(self):
        if self._peek().lexeme == "any":
            self._advance()
            idf = self._match_or_error(
                TT.ID, msg="Expected identifier in wildcard.")
            if self._peek().lexeme == "where":
                self._advance()
                cond = self.p_expr()
                e1 = ast.Wildcard(idf, cond)
            else:
                e1 = ast.Wildcard(idf, None)
        else:
            e1 = self.p_expr()
        self._match_or_error(
            TT.ARROW, msg="Expected arrow in map element.")
        e2 = self.p_expr()
        return (e1, e2)
