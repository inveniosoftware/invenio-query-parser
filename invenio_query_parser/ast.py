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

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit(self,
                             self.left.accept(visitor),
                             self.right.accept(visitor))

    def __eq__(self, other):
        return (
            type(self) == type(other)
        ) and (
            self.left == other.left
        ) and (
            self.right == other.right
        )

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__,
                               repr(self.left), repr(self.right))


class UnaryOp(object):

    def __init__(self, op):
        self.op = op

    def accept(self, visitor):
        return visitor.visit(self, self.op.accept(visitor))

    def __eq__(self, other):
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.op))


class ListOp(object):

    def __init__(self, children):
        try:
            iter(children)
        except TypeError:
            self.children = [children]
        else:
            self.children = children

    def accept(self, visitor):
        return visitor.visit(self, [c.accept(visitor) for c in self.children])

    def __eq__(self, other):
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.children))


class Leaf(object):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))


# Concrete classes

class BinaryKeywordBase(BinaryOp):
    @property
    def keyword(self):
        # FIXME evaluate if it's possible to move it out to spires module
        from .contrib.spires.ast import SpiresOp
        if self.left:
            if isinstance(self.left, SpiresOp):
                return self.left.keyword
        elif isinstance(self.right, SpiresOp):
            return self.right.keyword
        return None


class AndOp(BinaryKeywordBase):
    pass


class OrOp(BinaryKeywordBase):
    pass


class NotOp(UnaryOp):
    @property
    def keyword(self):
        return getattr(self.op, 'keyword')


class RangeOp(BinaryOp):
    pass


class LowerOp(UnaryOp):
    pass


class LowerEqualOp(UnaryOp):
    pass


class GreaterOp(UnaryOp):
    pass


class GreaterEqualOp(UnaryOp):
    pass


class KeywordOp(BinaryOp):
    pass


class NestedKeywordsRule(BinaryOp):
    pass


class ValueQuery(UnaryOp):
    pass


class Keyword(Leaf):
    pass


class Value(Leaf):
    pass


class SingleQuotedValue(Leaf):
    pass


class DoubleQuotedValue(Leaf):
    pass


class RegexValue(Leaf):
    pass


class EmptyQuery(Leaf):
    pass
