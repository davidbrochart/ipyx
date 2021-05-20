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

    def __init__(self, value=None):
        self.v = value

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value
