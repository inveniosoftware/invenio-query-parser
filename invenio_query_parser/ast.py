# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014, 2016 CERN.
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

"""Define abstract classes."""


class BinaryOp(object):
    """Base class for nodes with two operands."""

    def __init__(self, left, right):
        """Store left and right operands."""
        self.left = left
        self.right = right

    def accept(self, visitor):
        """Visit both operands, then this node."""
        return visitor.visit(self,
                             self.left.accept(visitor),
                             self.right.accept(visitor))

    def __eq__(self, other):
        """Compare node type and operands."""
        return (
            type(self) == type(other)
        ) and (
            self.left == other.left
        ) and (
            self.right == other.right
        )

    def __repr__(self):
        """Return constructor-like representation."""
        return "%s(%s, %s)" % (self.__class__.__name__,
                               repr(self.left), repr(self.right))


class UnaryOp(object):
    """Base class for nodes with one operand."""

    def __init__(self, op):
        """Store the operand."""
        self.op = op

    def accept(self, visitor):
        """Visit the operand, then this node."""
        return visitor.visit(self, self.op.accept(visitor))

    def __eq__(self, other):
        """Compare node type and operands."""
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        """Return constructor-like representation."""
        return "%s(%s)" % (self.__class__.__name__, repr(self.op))


class ListOp(object):
    """Base class for nodes with a list of children."""

    def __init__(self, children):
        """Store children, wrapping a single child in a list."""
        try:
            iter(children)
        except TypeError:
            self.children = [children]
        else:
            self.children = children

    def accept(self, visitor):
        """Visit all children, then this node."""
        return visitor.visit(self, [c.accept(visitor) for c in self.children])

    def __eq__(self, other):
        """Compare with another node."""
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        """Return constructor-like representation."""
        return "%s(%s)" % (self.__class__.__name__, repr(self.children))


class Leaf(object):
    """Base class for nodes holding a single value."""

    def __init__(self, value):
        """Store the value."""
        self.value = value

    def accept(self, visitor):
        """Visit this node."""
        return visitor.visit(self)

    def __eq__(self, other):
        """Compare node type and value."""
        return type(self) == type(other) and self.value == other.value

    def __repr__(self):
        """Return constructor-like representation."""
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))


# Concrete classes

class BinaryKeywordBase(BinaryOp):
    """Binary operation exposing a SPIRES keyword."""

    @property
    def keyword(self):
        """Return keyword of the SPIRES operand, if any."""
        # FIXME evaluate if it's possible to move it out to spires module
        from .contrib.spires.ast import SpiresOp
        if self.left:
            if isinstance(self.left, SpiresOp):
                return self.left.keyword
        elif isinstance(self.right, SpiresOp):
            return self.right.keyword
        return None


class AndOp(BinaryKeywordBase):
    """Logical AND of two queries."""


class OrOp(BinaryKeywordBase):
    """Logical OR of two queries."""


class NotOp(UnaryOp):
    """Logical negation of a query."""

    @property
    def keyword(self):
        """Return keyword of the negated query."""
        return getattr(self.op, 'keyword')


class RangeOp(BinaryOp):
    """Inclusive range between two values."""


class LowerOp(UnaryOp):
    """Lower than comparison."""


class LowerEqualOp(UnaryOp):
    """Lower than or equal comparison."""


class GreaterOp(UnaryOp):
    """Greater than comparison."""


class GreaterEqualOp(UnaryOp):
    """Greater than or equal comparison."""


class KeywordOp(BinaryOp):
    """Query restricted to a keyword."""


class NestedKeywordsRule(BinaryOp):
    """Chain of nested keywords."""


class ValueQuery(UnaryOp):
    """Query consisting of a value only."""


class Keyword(Leaf):
    """Keyword name."""


class Value(Leaf):
    """Unquoted value."""


class SingleQuotedValue(Leaf):
    """Single-quoted value."""


class DoubleQuotedValue(Leaf):
    """Double-quoted value."""


class RegexValue(Leaf):
    """Regular expression value."""


class EmptyQuery(Leaf):
    """Empty query."""
