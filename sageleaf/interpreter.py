from dataclasses import dataclass

from sageleaf import parser as p


@dataclass
class RuntimeEnvironment:
    types: dict[str, type]
    bindings: dict[str, float]


BASE_TYPES = {
    "Real": float
}

BASE_BINDINGS = {}


def interpret(tree: p.SyntaxTree) -> None:
    environment = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)
    for statement in tree.statements:
        environment = interpret_statement(environment, statement)


def interpret_statement(environment: RuntimeEnvironment, statement: p.Statement) -> RuntimeEnvironment:
    if isinstance(statement, p.Expression):
        print(evaluate_expression(environment, statement))
        return environment
    elif isinstance(statement, p.Binding):
        return interpret_binding(environment, statement)
    else:
        raise Exception(f"Unrecognised statement type {type(statement)}.")


def evaluate_expression(environment: RuntimeEnvironment, expression: p.Expression) -> float:
    if isinstance(expression, p.Real):
        return expression.value
    elif isinstance(expression, p.Identifier):
        if expression not in environment.bindings:
            raise Exception(f"Undefined binding {expression}.")
        return environment.bindings[expression]
    else:
        raise Exception(f"Unrecognised expression type {type(expression)}.")


def interpret_binding(environment: RuntimeEnvironment, binding: p.Binding) -> RuntimeEnvironment:
    if binding.type.identifier not in environment.types:
        raise Exception(f"Undefined type specified {binding.type.identifier}.")

    value = evaluate_expression(environment, binding.expression)
    environment.bindings[binding.identifier] = value

    return environment
