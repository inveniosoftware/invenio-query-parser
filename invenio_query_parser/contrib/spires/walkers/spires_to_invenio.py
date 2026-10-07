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

"""Implement query printer."""

from invenio_query_parser import ast
from invenio_query_parser.contrib.spires.config import SPIRES_KEYWORDS
from invenio_query_parser.visitor import make_visitor

from ..ast import SpiresOp


class SpiresToInvenio(object):
    """Convert a SPIRES AST to an Invenio AST."""

    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(ast.AndOp)
    def visit(self, node, left, right):
        """Convert ``AndOp`` node to Invenio AST."""
        return type(node)(left, right)

    @visitor(ast.OrOp)
    def visit(self, node, left, right):
        """Convert ``OrOp`` node to Invenio AST."""
        return type(node)(left, right)

    @visitor(ast.KeywordOp)
    def visit(self, node, left, right):
        """Convert ``KeywordOp`` node to Invenio AST."""
        return type(node)(left, right)

    @visitor(ast.RangeOp)
    def visit(self, node, left, right):
        """Convert ``RangeOp`` node to Invenio AST."""
        return type(node)(left, right)

    @visitor(ast.NotOp)
    def visit(self, node, op):
        """Convert ``NotOp`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.GreaterOp)
    def visit(self, node, op):
        """Convert ``GreaterOp`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.LowerOp)
    def visit(self, node, op):
        """Convert ``LowerOp`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.GreaterEqualOp)
    def visit(self, node, op):
        """Convert ``GreaterEqualOp`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.LowerEqualOp)
    def visit(self, node, op):
        """Convert ``LowerEqualOp`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.Keyword)
    def visit(self, node):
        """Convert ``Keyword`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(ast.Value)
    def visit(self, node):
        """Convert ``Value`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(ast.ValueQuery)
    def visit(self, node, op):
        """Convert ``ValueQuery`` node to Invenio AST."""
        return type(node)(op)

    @visitor(ast.SingleQuotedValue)
    def visit(self, node):
        """Convert ``SingleQuotedValue`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(ast.DoubleQuotedValue)
    def visit(self, node):
        """Convert ``DoubleQuotedValue`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(ast.RegexValue)
    def visit(self, node):
        """Convert ``RegexValue`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(ast.EmptyQuery)
    def visit(self, node):
        """Convert ``EmptyQuery`` node to Invenio AST."""
        return type(node)(node.value)

    @visitor(SpiresOp)
    def visit(self, node, left, right):
        """Convert ``SpiresOp`` node to Invenio AST."""
        left.value = SPIRES_KEYWORDS[left.value]
        return ast.KeywordOp(left, right)

    # pylint: enable=W0612,E0102
