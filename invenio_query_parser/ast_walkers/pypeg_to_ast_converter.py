# -*- coding: utf-8 -*-
#
# This file is part of Invenio Query Parser.
# Copyright (C) 2014 CERN.
#
# Invenio Query Parser is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio Query Parser is distributed in the hope that it will be useful,
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
from ..contrib.spires import parser as spires_parser
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

    @visitor(spires_parser.SpiresKeywordRule)
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

    @visitor(spires_parser.GreaterQuery)
    def visit(self, node, child):
        return ast.GreaterOp(child)

    @visitor(spires_parser.GreaterEqualQuery)
    def visit(self, node, child):
        return ast.GreaterEqualOp(child)

    @visitor(spires_parser.LowerQuery)
    def visit(self, node, child):
        return ast.LowerOp(child)

    @visitor(spires_parser.LowerEqualQuery)
    def visit(self, node, child):
        return ast.LowerEqualOp(child)

    @visitor(parser.Number)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.Value)
    def visit(self, node, child):
        return child

    @visitor(parser.NestableKeyword)
    def visit(self, node):
        return ast.Keyword(node.value)

    @visitor(spires_parser.SpiresSimpleValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(spires_parser.SpiresValue)
    def visit(self, node, children):
        return ast.Value("".join([c.value for c in children]))

    @visitor(spires_parser.SpiresValueQuery)
    def visit(self, node, child):
        return ast.ValueQuery(child)

    @visitor(spires_parser.SpiresSimpleQuery)
    def visit(self, node, child):
        return child

    @visitor(spires_parser.SpiresParenthesizedQuery)
    def visit(self, node, child):
        return child

    @visitor(spires_parser.SpiresNotQuery)
    def visit(self, node, child):
        return ast.AndOp(None, ast.NotOp(child))

    @visitor(spires_parser.SpiresAndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(spires_parser.SpiresOrQuery)
    def visit(self, node, child):
        return ast.OrOp(None, child)

    @visitor(parser.ValueQuery)
    def visit(self, node, child):
        return ast.ValueQuery(child)

    @visitor(spires_parser.SpiresKeywordQuery)
    def visit(self, node, keyword, value):
        return ast.SpiresOp(keyword, value)

    @visitor(parser.KeywordQuery)
    def visit(self, node, keyword, value):
        return ast.KeywordOp(keyword, value)

    @visitor(parser.SimpleQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.ParenthesizedQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.NotQuery)
    def visit(self, node, child):
        return ast.AndOp(None, ast.NotOp(child))

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

    @visitor(spires_parser.SpiresQuery)
    def visit(self, node, children):
        # Assign implicit keyword
        # find author x and y --> find author x and author y

        def assign_implicit_keyword(implicit_keyword, node):
            """
            Note: this function has side effects on node content
            """
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.ValueQuery:
                node.right = ast.SpiresOp(implicit_keyword, node.right.op)
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.NotOp:
                assign_implicit_keyword(implicit_keyword, node.right)
            if type(node) in [ast.NotOp] and \
               type(node.op) == ast.ValueQuery:
                node.op = ast.SpiresOp(implicit_keyword, node.op.op)

        implicit_keyword = None
        for child in children:
            new_keyword = getattr(child, 'keyword', None)
            if new_keyword is not None:
                implicit_keyword = new_keyword
            if implicit_keyword is not None:
                assign_implicit_keyword(implicit_keyword, child)

        # Build the boolean expression, left to right
        # x and y or z and ... --> ((x and y) or z) and ...
        tree = children[0]
        for booleanNode in children[1:]:
            booleanNode.left = tree
            tree = booleanNode
        return tree

    @visitor(spires_parser.FindQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.EmptyQueryRule)
    def visit(self, node):
        return ast.EmptyQuery(node.value)

    @visitor(parser.Main)
    def visit(self, node, child):
        return child

    @visitor(spires_parser.Main)
    def visit(self, node, child):
        return child

    # pylint: enable=W0612,E0102
