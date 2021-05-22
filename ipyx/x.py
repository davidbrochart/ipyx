#!/usr/bin/env python
# coding: utf-8

# Copyright (c) David Brochart.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from typing import Any, List

from ipywidgets import DOMWidget  # type: ignore
from traitlets import Unicode  # type: ignore
from ._frontend import module_name, module_version


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

    def _add(self, x0: "X", x1: "X") -> "X":
        x = X(
            inputs=[x0, x1], operation="self.v = self._inputs[0].v + self._inputs[1].v"
        )
        x._compute()
        self._outputs.append(x)
        return x

    def __add__(self, other: Any) -> "X":
        return self._add(self, make_x(other))

    def __radd__(self, other: Any) -> "X":
        return self._add(make_x(other), self)


def make_x(v: Any) -> X:
    if type(v) is X:
        return v
    return X(v)
