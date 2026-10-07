# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014 CERN.
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

"""SPIRES extended Pypeg to AST converter."""

from invenio_query_parser import ast
from invenio_query_parser.visitor import make_visitor
from invenio_query_parser.walkers import pypeg_to_ast

from .. import parser
from ..ast import SpiresOp


class PypegConverter(pypeg_to_ast.PypegConverter):
    """Convert a SPIRES pypeg2 parse tree to an AST."""

    visitor = make_visitor(pypeg_to_ast.PypegConverter.visitor)

    # pylint: disable=W0613,E0102

    @visitor(parser.SpiresKeywordRule)
    def visit(self, node):
        """Convert ``SpiresKeywordRule`` parse node to AST."""
        return ast.Keyword(node.value)

    @visitor(parser.SpiresKeywordQuery)
    def visit(self, node, keyword, value):
        """Convert ``SpiresKeywordQuery`` parse node to AST."""
        return SpiresOp(keyword, value)

    @visitor(parser.GreaterQuery)
    def visit(self, node, child):
        """Convert ``GreaterQuery`` parse node to AST."""
        return ast.GreaterOp(child)

    @visitor(parser.GreaterEqualQuery)
    def visit(self, node, child):
        """Convert ``GreaterEqualQuery`` parse node to AST."""
        return ast.GreaterEqualOp(child)

    @visitor(parser.LowerQuery)
    def visit(self, node, child):
        """Convert ``LowerQuery`` parse node to AST."""
        return ast.LowerOp(child)

    @visitor(parser.LowerEqualQuery)
    def visit(self, node, child):
        """Convert ``LowerEqualQuery`` parse node to AST."""
        return ast.LowerEqualOp(child)

    @visitor(parser.SpiresSimpleValue)
    def visit(self, node):
        """Convert ``SpiresSimpleValue`` parse node to AST."""
        return ast.Value(node.value)

    @visitor(parser.SpiresValue)
    def visit(self, node, children):
        """Convert ``SpiresValue`` parse node to AST."""
        return ast.Value("".join([c.value for c in children]))

    @visitor(parser.SpiresValueQuery)
    def visit(self, node, child):
        """Convert ``SpiresValueQuery`` parse node to AST."""
        return ast.ValueQuery(child)

    @visitor(parser.SpiresSimpleQuery)
    def visit(self, node, child):
        """Convert ``SpiresSimpleQuery`` parse node to AST."""
        return child

    @visitor(parser.SpiresParenthesizedQuery)
    def visit(self, node, child):
        """Convert ``SpiresParenthesizedQuery`` parse node to AST."""
        return child

    @visitor(parser.SpiresNotQuery)
    def visit(self, node, child):
        """Convert ``SpiresNotQuery`` parse node to AST."""
        return ast.AndOp(None, ast.NotOp(child))

    @visitor(parser.SpiresAndQuery)
    def visit(self, node, child):
        """Convert ``SpiresAndQuery`` parse node to AST."""
        return ast.AndOp(None, child)

    @visitor(parser.SpiresOrQuery)
    def visit(self, node, child):
        """Convert ``SpiresOrQuery`` parse node to AST."""
        return ast.OrOp(None, child)

    @visitor(parser.SpiresQuery)
    def visit(self, node, children):
        """Convert ``SpiresQuery`` parse node to AST."""
        # Assign implicit keyword
        # find author x and y --> find author x and author y

        def assign_implicit_keyword(implicit_keyword, node):
            """Assign implicit keyword to node (modifies node in place)."""
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.ValueQuery:
                node.right = SpiresOp(implicit_keyword, node.right.op)
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.NotOp:
                assign_implicit_keyword(implicit_keyword, node.right)
            if type(node) in [ast.NotOp] and \
               type(node.op) == ast.ValueQuery:
                node.op = SpiresOp(implicit_keyword, node.op.op)

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

    @visitor(parser.FindQuery)
    def visit(self, node, child):
        """Convert ``FindQuery`` parse node to AST."""
        return child

    @visitor(parser.Main)
    def visit(self, node, child):
        """Convert ``Main`` parse node to AST."""
        return child

    # pylint: enable=W0612,E0102
