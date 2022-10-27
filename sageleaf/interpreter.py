from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
from typing import Optional, Callable, Any, TypeAlias
from numbers import Real

from sageleaf import parser as p


PythonValue: TypeAlias = str | int | float | bool | Callable


@dataclass
class PrimitiveType:
    name: str
    is_member: Callable[[PythonValue], bool]
    effectful: bool = False


@dataclass
class FunctionType:
    name: str
    input_type: Type
    output_type: Type
    is_member: Callable[[PythonValue], bool]
    effectful: bool = False


Type: TypeAlias = PrimitiveType | FunctionType


@dataclass
class Value:
    type: Type
    python_value: PythonValue


@dataclass
class RuntimeEnvironment:
    types: dict[str, Type]
    bindings: dict[str, Value]


BASE_TYPES = {
    "Void": PrimitiveType("Any", lambda _: False),
    "Any": PrimitiveType("Any", lambda _: True),
    "Unit": PrimitiveType("Unit", lambda x: x == "Unit"),
    "Real": PrimitiveType("Real", lambda x: isinstance(x, (float, int))),
}

BASE_BINDINGS = {
    "Unit": Value(BASE_TYPES["Unit"], "Unit"),
    "add": Value(
        FunctionType(
            "Real -> Real -> Real",
            BASE_TYPES["Real"],
            FunctionType(
                "Real -> Real",
                BASE_TYPES["Real"],
                BASE_TYPES["Real"],
                lambda x: isinstance(x, Callable)
            ),
            lambda x: isinstance(x, Callable)
        ),
        lambda x: lambda y: x + y
    ),
    "print": Value(
        FunctionType(
            "Any -> Unit",
            BASE_TYPES["Any"],
            BASE_TYPES["Unit"],
            lambda x: isinstance(x, Callable)
        ),
        lambda x: [print(x), "Unit"][-1]
    ),
}


def interpret(tree: p.SyntaxTree) -> None:
    environment = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)
    value = evaluate_expression(environment, tree.expression)
    print(value)


def interpret_statement(
        environment: RuntimeEnvironment,
        statement: p.Statement) -> tuple[RuntimeEnvironment, Value]:
    if isinstance(statement, p.Expression):
        value = evaluate_expression(environment, statement)
        return environment, value
    elif isinstance(statement, p.Binding):
        return interpret_binding(environment, statement), BASE_BINDINGS["Unit"]
    else:
        raise Exception(f"Unrecognised statement type {type(statement)}.")


def evaluate_expression(environment: RuntimeEnvironment,
                        expression: p.Expression) -> Value:
    value = None
    for idx in range(len(expression.terms)):
        new_value = evaluate_term(environment, expression.terms[idx])
        if value is None:
            value = new_value
        else:
            value = evaluate_application(value, new_value)
    return value


def evaluate_application(function: Value, parameter: Value) -> Value:
    if isinstance(function.type, FunctionType):
        if function.type.input_type.is_member(parameter.python_value):
            python_value = function.python_value(parameter.python_value)
            output_type = function.type.output_type
            return Value(output_type, python_value)
        else:
            raise Exception(
                f"Function {function} expected a parameter of type {function.type.input_type}.")
    else:
        raise Exception(
            f"Attempting to apply a non-function type {function.type}.")


def evaluate_term(environment: RuntimeEnvironment, term: p.Term) -> Value:
    if isinstance(term, p.Real):
        return Value(BASE_TYPES["Real"], term.value)
    elif isinstance(term, p.Identifier):
        if term.name not in environment.bindings:
            raise Exception(f"Undefined binding {term.name}.")
        return environment.bindings[term.name]
    elif isinstance(term, p.Block):
        block_environment = deepcopy(environment)
        last_value = BASE_BINDINGS["Unit"]
        for statement in term.statements:
            block_environment, last_value = interpret_statement(
                block_environment, statement)
        return last_value
    else:
        raise Exception(
            f"Unrecognised term type {type(term)}.")


def interpret_binding(environment: RuntimeEnvironment,
                      binding: p.Binding) -> RuntimeEnvironment:
    if binding.type.identifier.name not in environment.types:
        raise Exception(
            f"Undefined type specified {binding.type.identifier.name}.")
    binding_type = environment.types[binding.type.identifier.name]
    value = evaluate_expression(environment, binding.expression)

    # Type check that the value is a member of the specified type.
    if binding_type.is_member(value.python_value):
        environment.bindings[binding.identifier.name] = Value(
            binding_type, value.python_value)
    else:
        raise Exception(
            f"Binding to `{binding.identifier.name}` expected a value of type {binding_type}.")

    return environment
