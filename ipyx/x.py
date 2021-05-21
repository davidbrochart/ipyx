#!/usr/bin/env python
# coding: utf-8

# Copyright (c) David Brochart.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import module_name, module_version


class X(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('XModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('XView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _value = Unicode('None').tag(sync=True)

    def __init__(self, value=None, inputs=[], operation="", **kwargs):
        self._outputs = []
        self._inputs = inputs
        self._operation = operation
        self.v = value
        super(X, self).__init__(**kwargs)

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value
        self._value = str(value)
        for x in self._outputs:
            x._compute()

    def _compute(self):
        if self._operation:
            exec(self._operation)

    def __add__(self, other):
        x = X(inputs=[self, X(other)], operation="self.v = self._inputs[0].v + self._inputs[1].v")
        x._compute()
        self._outputs.append(x)
        return x

    def __radd__(self, other):
        return self.__add__(other)
