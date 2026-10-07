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

"""Implement representation printer."""

from ..ast import AndOp, DoubleQuotedValue, EmptyQuery, GreaterEqualOp, \
    GreaterOp, Keyword, KeywordOp, LowerEqualOp, LowerOp, NotOp, OrOp, \
    RangeOp, RegexValue, SingleQuotedValue, Value, ValueQuery
from ..visitor import make_visitor


class TreeRepr(object):
    """Print a representation of an AST."""

    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(AndOp)
    def visit(self, node, left, right):
        """Return representation of ``AndOp`` node."""
        return '(%s and %s)' % (left, right)

    @visitor(OrOp)
    def visit(self, node, left, right):
        """Return representation of ``OrOp`` node."""
        return '(%s or %s)' % (left, right)

    @visitor(NotOp)
    def visit(self, node, op):
        """Return representation of ``NotOp`` node."""
        return '(not %s)' % op

    @visitor(KeywordOp)
    def visit(self, node, left, right):
        """Return representation of ``KeywordOp`` node."""
        return '%s:%s' % (left, right)

    @visitor(Keyword)
    def visit(self, node):
        """Return representation of ``Keyword`` node."""
        return '`%s`' % node.value

    @visitor(Value)
    def visit(self, node):
        """Return representation of ``Value`` node."""
        return "'%s'" % node.value

    @visitor(ValueQuery)
    def visit(self, node, query):
        """Return representation of ``ValueQuery`` node."""
        return query

    @visitor(SingleQuotedValue)
    def visit(self, node):
        """Return representation of ``SingleQuotedValue`` node."""
        return "'%s'" % node.value

    @visitor(DoubleQuotedValue)
    def visit(self, node):
        """Return representation of ``DoubleQuotedValue`` node."""
        return '"%s"' % node.value

    @visitor(RegexValue)
    def visit(self, node):
        """Return representation of ``RegexValue`` node."""
        return "/%s/" % node.value

    @visitor(RangeOp)
    def visit(self, node, left, right):
        """Return representation of ``RangeOp`` node."""
        return "%s->%s" % (left, right)

    @visitor(GreaterOp)
    def visit(self, node, op):
        """Return representation of ``GreaterOp`` node."""
        return '> %s' % op

    @visitor(GreaterEqualOp)
    def visit(self, node, op):
        """Return representation of ``GreaterEqualOp`` node."""
        return '>= %s' % op

    @visitor(LowerOp)
    def visit(self, node, op):
        """Return representation of ``LowerOp`` node."""
        return '< %s' % op

    @visitor(LowerEqualOp)
    def visit(self, node, op):
        """Return representation of ``LowerEqualOp`` node."""
        return '<= %s' % op

    @visitor(EmptyQuery)
    def visit(self, node):
        """Return representation of ``EmptyQuery`` node."""
        return '__empty__'

    # pylint: enable=W0612,E0102
