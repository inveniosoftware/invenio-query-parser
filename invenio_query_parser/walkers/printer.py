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

from ..ast import AndOp, DoubleQuotedValue, Keyword, KeywordOp, NotOp, OrOp, \
    RangeOp, RegexValue, SingleQuotedValue, Value
from ..visitor import make_visitor


class TreePrinter(object):
    """Print an AST as a query string."""

    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(AndOp)
    def visit(self, node, left, right):
        """Print ``AndOp`` node as query string."""
        return '(%s and %s)' % (left, right)

    @visitor(OrOp)
    def visit(self, node, left, right):
        """Print ``OrOp`` node as query string."""
        return '(%s or %s)' % (left, right)

    @visitor(NotOp)
    def visit(self, node, op):
        """Print ``NotOp`` node as query string."""
        return '(not %s)' % op

    @visitor(KeywordOp)
    def visit(self, node, left, right):
        """Print ``KeywordOp`` node as query string."""
        return '%s:%s' % (left, right)

    @visitor(Keyword)
    def visit(self, node):
        """Print ``Keyword`` node as query string."""
        return '%s' % node.value

    @visitor(Value)
    def visit(self, node):
        """Print ``Value`` node as query string."""
        return "%s" % node.value

    @visitor(SingleQuotedValue)
    def visit(self, node):
        """Print ``SingleQuotedValue`` node as query string."""
        return "'%s'" % node.value

    @visitor(DoubleQuotedValue)
    def visit(self, node):
        """Print ``DoubleQuotedValue`` node as query string."""
        return '"%s"' % node.value

    @visitor(RegexValue)
    def visit(self, node):
        """Print ``RegexValue`` node as query string."""
        return "/%s/" % node.value

    @visitor(RangeOp)
    def visit(self, node, left, right):
        """Print ``RangeOp`` node as query string."""
        return "%s->%s" % (left, right)

    # pylint: enable=W0612,E0102
