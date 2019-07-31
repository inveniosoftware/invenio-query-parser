# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Implement query printer."""

from invenio_query_parser import ast
from invenio_query_parser.contrib.spires.config import SPIRES_KEYWORDS
from invenio_query_parser.visitor import make_visitor

from ..ast import SpiresOp


class SpiresToInvenio(object):
    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(ast.AndOp)
    def visit(self, node, left, right):
        return type(node)(left, right)

    @visitor(ast.OrOp)
    def visit(self, node, left, right):
        return type(node)(left, right)

    @visitor(ast.KeywordOp)
    def visit(self, node, left, right):
        return type(node)(left, right)

    @visitor(ast.RangeOp)
    def visit(self, node, left, right):
        return type(node)(left, right)

    @visitor(ast.NotOp)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.GreaterOp)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.LowerOp)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.GreaterEqualOp)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.LowerEqualOp)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.Keyword)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(ast.Value)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(ast.ValueQuery)
    def visit(self, node, op):
        return type(node)(op)

    @visitor(ast.SingleQuotedValue)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(ast.DoubleQuotedValue)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(ast.RegexValue)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(ast.EmptyQuery)
    def visit(self, node):
        return type(node)(node.value)

    @visitor(SpiresOp)
    def visit(self, node, left, right):
        left.value = SPIRES_KEYWORDS[left.value]
        return ast.KeywordOp(left, right)

    # pylint: enable=W0612,E0102
