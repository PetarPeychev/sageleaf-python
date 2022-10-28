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

    def __str__(self: PrimitiveType) -> str:
        return self.name


@dataclass
class FunctionType:
    input_type: Type
    output_type: Type
    is_member: Callable[[PythonValue], bool]
    effectful: bool = False

    @property
    def name(self) -> str:
        left = str(self.input_type) if isinstance(
            self.input_type, PrimitiveType) else f"({self.input_type})"
        right = str(self.output_type) if isinstance(
            self.output_type, PrimitiveType) else f"({self.output_type})"
        return f"{left} -> {right}"

    def __str__(self: FunctionType) -> str:
        return self.name


Type: TypeAlias = PrimitiveType | FunctionType


@dataclass
class Value:
    type: Type
    python_value: PythonValue

    def __str__(self: Value) -> str:
        if isinstance(self.type, PrimitiveType):
            return f"{self.python_value} :: {self.type}"
        elif isinstance(self.type, FunctionType):
            return f"λ :: {self.type}"


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
            BASE_TYPES["Real"],
            FunctionType(
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
            BASE_TYPES["Any"],
            BASE_TYPES["Unit"],
            lambda x: isinstance(x, Callable)
        ),
        lambda x: [print(x), "Unit"][-1]
    ),
}


def interpret(tree: p.SyntaxTree) -> None:
    env = RuntimeEnvironment(BASE_TYPES, BASE_BINDINGS)
    value = evaluate_expr(env, tree.expression)
    print(value)


def interpret_statement(
        env: RuntimeEnvironment,
        statement: p.Statement) -> tuple[RuntimeEnvironment, Value]:
    if isinstance(statement, p.Expression):
        value = evaluate_expr(env, statement)
        return env, value
    elif isinstance(statement, p.Binding):
        return interpret_binding(env, statement), BASE_BINDINGS["Unit"]
    else:
        raise Exception(f"Unrecognised statement type {type(statement)}.")


def evaluate_expr(env: RuntimeEnvironment,
                  expr: p.Expression) -> Value:
    value = None
    for idx in range(len(expr.terms)):
        new_value = evaluate_term(env, expr.terms[idx])
        if value is None:
            value = new_value
        else:
            value = evaluate_application(value, new_value)
    return value


def evaluate_application(func: Value, parameter: Value) -> Value:
    if isinstance(func.type, FunctionType):
        if func.type.input_type.is_member(parameter.python_value):
            python_value = func.python_value(parameter.python_value)
            output_type = func.type.output_type
            return Value(output_type, python_value)
        else:
            raise Exception(
                f"Function {func} expected a parameter of type {func.type.input_type}.")
    else:
        raise Exception(
            f"Attempting to apply a non-function type {func.type}.")


def evaluate_term(env: RuntimeEnvironment, term: p.Term) -> Value:
    if isinstance(term, p.Real):
        return Value(BASE_TYPES["Real"], term.value)
    elif isinstance(term, p.Identifier):
        if term.name not in env.bindings:
            raise Exception(f"Undefined binding {term.name}.")
        return env.bindings[term.name]
    elif isinstance(term, p.Block):
        block_env = deepcopy(env)
        last_value = BASE_BINDINGS["Unit"]
        for statement in term.statements:
            block_env, last_value = interpret_statement(
                block_env, statement)
        return last_value
    else:
        raise Exception(
            f"Unrecognised term type {type(term)}.")


def interpret_binding(env: RuntimeEnvironment,
                      binding: p.Binding) -> RuntimeEnvironment:
    binding_type = interpret_type(env, binding.type)

    value = evaluate_expr(env, binding.expression)

    # Type check that the value is a member of the specified type.
    if binding_type.is_member(value.python_value):
        env.bindings[binding.identifier.name] = Value(
            binding_type, value.python_value)
    else:
        raise Exception(
            f"Binding to `{binding.identifier.name}` expected a value of type {binding_type}.")

    return env


def interpret_type(env: RuntimeEnvironment, type: p.Type) -> Type:
    if isinstance(type, p.PrimitiveType):
        if type.identifier.name in env.types:
            return env.types[type.identifier.name]
        else:
            raise Exception(f"Undefined type {type.identifier.name}.")
    else:
        return FunctionType(
            interpret_type(env, type.input_type),
            interpret_type(env, type.output_type),
            lambda x: isinstance(x, Callable)
        )
