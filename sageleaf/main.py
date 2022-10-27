from sageleaf.lexer import lex
from sageleaf.parser import parse_statement
from sageleaf.interpreter import BASE_BINDINGS, BASE_TYPES, RuntimeEnvironment, interpret_statement


def main() -> None:
    print("Sageleaf 1.0.0:")

    environment = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)

    while True:
        line = input("> ")
        tokens = lex(line)
        _, statement = parse_statement(0, tokens)
        environment = interpret_statement(environment, statement)
