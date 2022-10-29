import sys
from pathlib import Path

from sageleaf.lexer import lex
from sageleaf.parser import parse_statement, parse
from sageleaf.interpreter import (
    BASE_BINDINGS,
    BASE_TYPES,
    RuntimeEnvironment,
    interpret_statement,
    interpret,
)


def main() -> None:
    args = sys.argv[1:]

    if len(args) == 0:
        run_repl()
    elif len(args) == 1:
        interpret_file(args[0])


def run_repl() -> None:
    print("Sageleaf 1.0.0:")

    environment = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)

    while True:
        line = input("> ")
        try:
            tokens = lex(line)
            _, statement = parse_statement(0, tokens)
            environment, value = interpret_statement(environment, statement)
            print(value)
        except Exception as ex:
            print(ex)


def interpret_file(filename: str) -> None:
    contents = Path(filename).read_text()
    tokens = lex(contents)
    tree = parse(tokens)
    interpret(tree)
