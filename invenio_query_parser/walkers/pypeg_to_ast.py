# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Invenio-Query-Parser is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio-Query-Parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Implement Pypeg to AST converter."""

from .. import ast, parser
from ..visitor import make_visitor


class PypegConverter(object):
    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(parser.Whitespace)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.Not)
    def visit(self, node, child):
        return ast.NotOp(child)

    @visitor(parser.And)
    def visit(self, node, left, right):
        return ast.AndOp(left, right)

    @visitor(parser.Or)
    def visit(self, node, left, right):
        return ast.Or(left, right)

    @visitor(parser.KeywordRule)
    def visit(self, node):
        return ast.Keyword(node.value)

    @visitor(parser.SingleQuotedString)
    def visit(self, node):
        return ast.SingleQuotedValue(node.value)

    @visitor(parser.DoubleQuotedString)
    def visit(self, node):
        return ast.DoubleQuotedValue(node.value)

    @visitor(parser.SlashQuotedString)
    def visit(self, node):
        return ast.RegexValue(node.value)

    @visitor(parser.SimpleValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.SimpleRangeValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.RangeValue)
    def visit(self, node, child):
        return child

    @visitor(parser.RangeOp)
    def visit(self, node, left, right):
        return ast.RangeOp(left, right)

    @visitor(parser.Number)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.Value)
    def visit(self, node, child):
        return child

    @visitor(parser.ValueQuery)
    def visit(self, node, child):
        return ast.ValueQuery(child)

    @visitor(parser.KeywordQuery)
    def visit(self, node, keyword, value):
        return ast.KeywordOp(keyword, value)

    @visitor(parser.NotKeywordValue)
    def visit(self, node):
        return ast.ValueQuery(ast.Value(node.value))

    @visitor(parser.NestedKeywordsRule)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.SimpleQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.ParenthesizedQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.NotQuery)
    def visit(self, node, child):
        return ast.NotOp(child)

    @visitor(parser.AndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(parser.ImplicitAndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(parser.OrQuery)
    def visit(self, node, child):
        return ast.OrOp(None, child)

    @visitor(parser.Query)
    def visit(self, node, children):
        # Build the boolean expression, left to right
        # x and y or z and ... --> ((x and y) or z) and ...
        tree = children[0]
        for booleanNode in children[1:]:
            booleanNode.left = tree
            tree = booleanNode
        return tree

    @visitor(parser.EmptyQueryRule)
    def visit(self, node):
        return ast.EmptyQuery(node.value)

    @visitor(parser.Main)
    def visit(self, node, child):
        return child

    # pylint: enable=W0612,E0102
