from __future__ import annotations
from typing import TypeAlias, Optional
from dataclasses import dataclass

from sageleaf.lexer import Token, TokenType


@dataclass
class SyntaxTree:
    expression: Expression


@dataclass
class Binding:
    identifier: Identifier
    type: Type
    expression: Expression


# @dataclass
# class TypeDefinition:
#     identifier: str
#     body: TypeBody


@dataclass
class Block:
    statements: list[Statement]


@dataclass
class Real:
    value: float


@dataclass
class Identifier:
    name: str


@dataclass
class PrimitiveType:
    identifier: Identifier
    type_parameters: list[Identifier]


@dataclass
class FunctionType:
    input_type: Type
    output_type: Type


Type: TypeAlias = PrimitiveType | FunctionType

# @dataclass
# class TypeBody:
#     pass


@dataclass
class Expression:
    terms: list[Term]


Term: TypeAlias = Block | Real | Identifier

# Statement: TypeAlias = Binding | TypeDefinition | Expression
Statement: TypeAlias = Binding | Expression


def parse(tokens: list[Token]) -> SyntaxTree:
    idx: int = 0

    tokens = (
        [Token(TokenType.STARTBLOCK, None)] + tokens + [Token(TokenType.ENDBLOCK, None)]
    )

    _, expression = parse_expression(idx, tokens)

    return SyntaxTree(expression)


def parse_statement(idx: int, tokens: list[Token]) -> tuple[int, Statement]:
    statement = None
    if tokens[idx].type == TokenType.LET:
        idx, statement = parse_binding(idx, tokens)
    else:
        idx, statement = parse_expression(idx, tokens)
    idx, end = expect(idx, tokens, TokenType.BREAK)
    if end:
        return idx, statement
    else:
        raise Exception(f"Expected statement break at token index {idx}.")


def parse_binding(idx: int, tokens: list[Token]) -> tuple[int, Binding]:
    idx, _ = expect(idx, tokens, TokenType.LET)
    idx, name = expect(idx, tokens, TokenType.IDENTIFIER)
    if name:
        idx, colon = expect(idx, tokens, TokenType.COLON)
        if colon:
            idx, let_type = parse_type(idx, tokens)
            idx, assignment = expect(idx, tokens, TokenType.ASSIGN)
            if assignment:
                idx, expression = parse_expression(idx, tokens)
                return idx, Binding(Identifier(name.value), let_type, expression)
            else:
                raise Exception(f"Expected assignment at token index {idx}.")
        else:
            raise Exception(f"Expected colon at token index {idx}.")
    else:
        raise Exception(f"Expected identifier at token index {idx}.")


def parse_type(idx: int, tokens: list[Token]) -> tuple[int, Type]:
    idx, name = expect(idx, tokens, TokenType.IDENTIFIER)
    if name:
        first_type = PrimitiveType(Identifier(name.value), [])
        idx, arrow = expect(idx, tokens, TokenType.ARROW)
        if arrow:
            idx, second_type = parse_type(idx, tokens)
            return idx, FunctionType(first_type, second_type)
        else:
            return idx, first_type
    else:
        raise Exception(f"Expected type identifier at token index {idx}.")


def parse_expression(idx: int, tokens: list[Token]) -> tuple[int, Expression]:
    terms = []
    while idx < len(tokens) and tokens[idx].type != TokenType.BREAK:
        idx, term = parse_term(idx, tokens)
        terms.append(term)
    if len(terms) < 1:
        raise Exception(f"Expected one or more terms at token index {idx}.")
    return idx, Expression(terms)


def parse_term(idx: int, tokens: list[Token]) -> tuple[int, Term]:
    idx, start = expect(idx, tokens, TokenType.STARTBLOCK)
    if start:
        idx, block = parse_block(idx, tokens)
        idx, end = expect(idx, tokens, TokenType.ENDBLOCK)
        if end:
            return idx, block
        else:
            raise Exception(f"Expected end of block at token index {idx}.")
    else:
        idx, number = expect(idx, tokens, TokenType.NUMBER)
        if number:
            return idx, Real(float(number.value))
        else:
            idx, identifier = expect(idx, tokens, TokenType.IDENTIFIER)
            if identifier:
                return idx, Identifier(identifier.value)
            else:
                raise Exception(f"Unrecognised term at token index {idx}.")


def parse_block(idx: int, tokens: list[Token]) -> tuple[int, Block]:
    statements: list[Statement] = []

    while idx < len(tokens) and tokens[idx].type != TokenType.ENDBLOCK:
        idx, statement = parse_statement(idx, tokens)
        statements.append(statement)

    return idx, Block(statements)


def expect(
    idx: int, tokens: list[Token], type: TokenType
) -> tuple[int, Optional[Token]]:
    if idx < len(tokens) and tokens[idx].type == type:
        return idx + 1, tokens[idx]
    else:
        return idx, None
