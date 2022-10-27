from dataclasses import dataclass
from copy import deepcopy
from typing import Optional

from sageleaf import parser as p


@dataclass
class RuntimeEnvironment:
    types: dict[str, type]
    bindings: dict[str, float]


BASE_TYPES = {"Real": float}

BASE_BINDINGS = {}


def interpret(tree: p.SyntaxTree) -> None:
    environment = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)
    value = evaluate_expression(environment, tree.expression)
    print(value)


def interpret_statement(
        environment: RuntimeEnvironment,
        statement: p.Statement) -> tuple[RuntimeEnvironment, Optional[float]]:
    if isinstance(statement, p.Expression):
        value = evaluate_expression(environment, statement)
        return environment, value
    elif isinstance(statement, p.Binding):
        return interpret_binding(environment, statement), None
    else:
        raise Exception(f"Unrecognised statement type {type(statement)}.")


def evaluate_expression(environment: RuntimeEnvironment,
                        expression: p.Expression) -> float:
    if isinstance(expression.value, p.Real):
        return expression.value
    elif isinstance(expression.value, p.Identifier):
        if expression.value.name not in environment.bindings:
            raise Exception(f"Undefined binding {expression.value.name}.")
        return environment.bindings[expression.value.name]
    elif isinstance(expression.value, p.Block):
        block_environment = deepcopy(environment)
        last_value = None
        for statement in expression.value.statements:
            block_environment, value = interpret_statement(
                block_environment, statement)
            if value is not None:
                last_value = value
        return last_value
    else:
        raise Exception(f"Unrecognised expression type {type(expression)}.")


def interpret_binding(environment: RuntimeEnvironment,
                      binding: p.Binding) -> RuntimeEnvironment:
    if binding.type.identifier.name not in environment.types:
        raise Exception(f"Undefined type specified {binding.type.identifier.name}.")

    value = evaluate_expression(environment, binding.expression)
    environment.bindings[binding.identifier.name] = value

    return environment
