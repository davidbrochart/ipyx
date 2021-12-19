#!/usr/bin/env python
# coding: utf-8

# Copyright (c) David Brochart.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from typing import Any, List, Dict, Callable, Optional

from ipycytoscape import CytoscapeWidget  # type: ignore
from ipywidgets import DOMWidget  # type: ignore
from traitlets import Unicode, Bool  # type: ignore
from ._frontend import module_name, module_version


class W(DOMWidget):
    """TODO: Add docstring here"""

    _model_name = Unicode("XModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("XView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _value = Unicode("None").tag(sync=True)
    _computing = Bool(False).tag(sync=True)


class X:
    _i = 0

    @classmethod
    def new_id(cls):
        name = str(cls._i)
        cls._i += 1
        return name

    def __init__(
        self,
        v: Any = None,
        n: str = "",
        _inputs: List["X"] = [],
        _kwinputs: Dict[str, "X"] = {},
        _operation: str = "",
        _function: Optional[Callable] = None,
        _fname: Optional[str] = None,
        **kwargs,
    ):
        self._outputs: List[X] = []
        self._inputs = _inputs
        self._kwinputs = _kwinputs
        self._operation = _operation
        self._function = _function
        self._fname = _fname
        self._w: Optional[W] = None
        self._computing = False
        self.v = v
        self.n = n
        self.i = self.new_id()
        super(X, self).__init__(**kwargs)

    @property
    def w(self) -> W:
        if self._w is None:
            self._w = W()
            self._w._computing = self._computing
            self._w._value = str(self._v)
        return self._w

    @property
    def v(self) -> Any:
        return self._v

    @v.setter
    def v(self, v: Any) -> None:
        for x in self._outputs:
            x._set_computing()
        self._v = v
        self.computing = False
        if self._w is not None:
            self._w._computing = False
            self._w._value = str(v)
        for x in self._outputs:
            x._compute()

    def _compute(self) -> None:
        if self._operation:
            try:
                exec(self._operation)
            except Exception:
                pass

    def _set_computing(self) -> None:
        if not self._computing:
            self._computing = True
            if self._w is not None:
                self._w._computing = True
            for x in self._outputs:
                x._set_computing()

    def __repr__(self):
        return str(self._v)

    def visualize(self, dag: Optional[Dict] = None):
        show = not dag
        dag = dag or {
            "inputs": [],
            "output": self.i,
            "dag": {
                "nodes": [
                    {"data": {"id": self.i, "name": self.n, "tooltip": self._fname}}
                ],
                "edges": [],
            },
        }
        node_ids = [node["data"]["id"] for node in dag["dag"]["nodes"]]
        inputs = self._inputs + list(self._kwinputs.values())
        if not inputs and self.i not in dag["inputs"]:
            dag["inputs"].append(self.i)
        for i in inputs:
            if i.i not in node_ids:
                dag["dag"]["nodes"].append(
                    {"data": {"id": i.i, "name": i.n, "tooltip": i._fname}}
                )
            dag["dag"]["edges"].append({"data": {"source": i.i, "target": self.i}})
            i.visualize(dag)
        if show:
            graph = CytoscapeWidget()
            graph.graph.add_graph_from_json(dag["dag"])
            graph.set_tooltip_source("tooltip")
            style = [
                {
                    "selector": "node",
                    "css": {
                        "content": "data(name)",
                        "background-color": "green",
                        "text-valign": "center",
                        "color": "white",
                        "text-outline-width": 2,
                        "text-outline-color": "green",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "target-arrow-shape": "triangle",
                        "curve-style": "bezier",
                    },
                },
            ]
            for i in dag["inputs"]:
                style.append(
                    {
                        "selector": f'node[id = "{i}"]',
                        "style": {
                            "background-color": "blue",
                            "text-outline-color": "blue",
                        },
                    }
                )
            style.append(
                {
                    "selector": f'node[id = "{dag["output"]}"]',
                    "style": {"background-color": "red", "text-outline-color": "red"},
                }
            )
            graph.set_style(style)
            return graph


def make_x(v: Any) -> X:
    if isinstance(v, X):
        return v
    return X(v)


def register(func: Callable):
    def wrapper(self: X, inputs: List[X]) -> X:
        x = func(self, inputs)
        x._compute()
        for i in inputs:
            i._outputs.append(x)
        return x

    return wrapper


def make_unary(name: str, sign: str = ""):
    @register
    def operation(self, inputs: List[X]) -> X:
        if sign:
            expression = f"{sign}self._inputs[0].v"
        else:
            expression = f"{name}(self._inputs[0].v)"
        return X(_inputs=inputs, _operation=f"self.v = {expression}")

    def normal(self) -> X:
        return operation(self, [self])

    setattr(X, f"__{name}__", normal)


def make_binary(name: str, sign: str = ""):
    @register
    def operation(self, inputs: List[X]) -> X:
        if sign:
            expression = f"self._inputs[0].v {sign} self._inputs[1].v"
            fname = sign
        else:
            expression = f"{name}(self._inputs[0].v, self._inputs[1].v)"
            fname = name
        return X(_inputs=inputs, _operation=f"self.v = {expression}", _fname=fname)

    def normal(self, other: Any) -> X:
        return operation(self, [self, make_x(other)])

    def reflected(self, other: Any) -> X:
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
