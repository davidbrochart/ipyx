#!/usr/bin/env python
# coding: utf-8

# Copyright (c) David Brochart.
# Distributed under the terms of the Modified BSD License.

from ..x import X


def test_x_creation_blank():
    x = X()
    assert x.v is None
