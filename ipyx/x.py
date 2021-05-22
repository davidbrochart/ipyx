#!/usr/bin/env python
# coding: utf-8

# Copyright (c) David Brochart.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from typing import Any, List, Callable

from ipywidgets import DOMWidget  # type: ignore
from traitlets import Unicode  # type: ignore
from ._frontend import module_name, module_version


def make_x(v: Any) -> "X":
    if type(v) is X:
        return v
    return X(v)


def register(func: Callable):
    def wrapper(self: "X", inputs: List["X"]) -> "X":
        x = func(self, inputs)
        x._compute()
        self._outputs.append(x)
        return x

    return wrapper


class X(DOMWidget):
    """TODO: Add docstring here"""

    _model_name = Unicode("XModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("XView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _value = Unicode("None").tag(sync=True)

    def __init__(
        self, value: Any = None, inputs: List["X"] = [], operation: str = "", **kwargs
    ):
        self._outputs: List[X] = []
        self._inputs = inputs
        self._operation = operation
        self.v = value
        super(X, self).__init__(**kwargs)

    @property
    def v(self) -> Any:
        return self._v

    @v.setter
    def v(self, value: Any) -> None:
        self._v = value
        self._value = str(value)
        for x in self._outputs:
            x._compute()

    def _compute(self) -> None:
        if self._operation:
            exec(self._operation)


def make_unary(name: str, sign: str = ""):
    @register
    def operation(self, inputs: List["X"]) -> "X":
        if sign:
            expression = f"{sign}self._inputs[0].v"
        else:
            expression = f"{name}(self._inputs[0].v)"
        return X(inputs=inputs, operation=f"self.v = {expression}")

    def normal(self) -> "X":
        return operation(self, [self])

    setattr(X, f"__{name}__", normal)


def make_binary(name: str, sign: str = ""):
    @register
    def operation(self, inputs: List["X"]) -> "X":
        if sign:
            expression = f"self._inputs[0].v {sign} self._inputs[1].v"
        else:
            expression = f"{name}(self._inputs[0].v, self._inputs[1].v)"
        return X(inputs=inputs, operation=f"self.v = {expression}")

    def normal(self, other: Any) -> "X":
        return operation(self, [self, make_x(other)])

    def reflected(self, other: Any) -> "X":
        return operation(self, [make_x(other), self])

    setattr(X, f"_{name}", operation)
    setattr(X, f"__{name}__", normal)
    setattr(X, f"__r{name}__", reflected)


make_unary("neg", "-")
make_unary("pos", "+")
make_unary("abs")
make_unary("invert", "~")
make_unary("complex")
make_unary("int")
make_unary("float")
# TODO: __index__ ?
make_unary("round")
make_unary("trunc")
make_unary("floor")
make_unary("ceil")

make_binary("add", "+")
make_binary("sub", "-")
make_binary("mul", "*")
make_binary("matmul", "@")
make_binary("truediv", "/")
make_binary("floordiv", "//")
make_binary("mod", "%")
make_binary("divmod")
make_binary("pow", "**")
make_binary("lshift", "<<")
make_binary("rshift", ">>")
make_binary("and", "&")
make_binary("xor", "^")
make_binary("or", "|")
