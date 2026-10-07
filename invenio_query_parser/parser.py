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

"""Define parsers."""

from __future__ import absolute_import

import re

import pypeg2
from pypeg2 import Keyword, Literal, attr, maybe_some, omit, optional, some

from . import ast
from ._compat import string_types

# pylint: disable=C0321,R0903


class LeafRule(ast.Leaf):
    """Base rule for leaf grammar nodes."""

    def __init__(self):
        """Initialize without arguments for pypeg2."""
        pass


class UnaryRule(ast.UnaryOp):
    """Base rule for grammar nodes with one operand."""

    def __init__(self):
        """Initialize without arguments for pypeg2."""
        pass


class BinaryRule(ast.BinaryOp):
    """Base rule for grammar nodes with two operands."""

    def __init__(self):
        """Initialize without arguments for pypeg2."""
        pass


class ListRule(ast.ListOp):
    """Base rule for grammar nodes with a list of children."""

    def __init__(self):
        """Initialize without arguments for pypeg2."""
        pass


class Whitespace(LeafRule):
    """Match one or more whitespace characters."""

    grammar = attr('value', re.compile(r"\s+"))


_ = optional(Whitespace)


class Not(object):
    """Match a negation operator (``NOT``, ``AND NOT`` or ``-``)."""

    grammar = omit([
        omit(re.compile(r"AND\s+NOT")),
        re.compile(r"NOT"),
        Literal('-'),
    ])


class And(object):
    """Match a conjunction operator (``AND`` or ``+``)."""

    grammar = omit([
        re.compile(r"AND"),
        Literal('+'),
    ])


class Or(object):
    """Match a disjunction operator (``OR`` or ``|``)."""

    grammar = omit([
        re.compile(r"OR"),
        Literal('|'),
    ])


class KeywordRule(LeafRule):
    """Match a keyword name, possibly dotted."""

    grammar = attr('value', re.compile(r"[\w\d]+(\.[\w\d]+)*"))


class NestedKeywordsRule(LeafRule):
    """Match a chain of colon-separated keywords."""

    grammar = attr('value', re.compile(
        r"(([\w\d]+(\.[\w\d]+)*):\s*)+([\w\d]+(\.[\w\d]+)*)"))


class SingleQuotedString(LeafRule):
    """Match a single-quoted string."""

    grammar = Literal("'"), attr('value', re.compile(r"([^']|\\.)*")), \
        Literal("'")


class DoubleQuotedString(LeafRule):
    """Match a double-quoted string."""

    grammar = Literal('"'), attr('value', re.compile(r'([^"]|\\.)*')), \
        Literal('"')


class SlashQuotedString(LeafRule):
    """Match a slash-delimited regular expression."""

    grammar = Literal('/'), attr('value', re.compile(r"([^/]|\\.)*")), \
        Literal('/')


class SimpleValue(LeafRule):
    """Match an unquoted value made of one or more units."""

    def __init__(self, values):
        """Join matched units into a single value."""
        super(SimpleValue, self).__init__()
        self.value = "".join(v.value for v in values)


class SimpleValueUnit(LeafRule):
    """Match an unquoted value unit."""

    grammar = [
        re.compile(r"[^\s\)\(:]+"),
        (re.compile(r'\('), SimpleValue, re.compile(r'\)')),
    ]

    def __init__(self, args):
        """Build value from a string or a parenthesized group."""
        super(SimpleValueUnit, self).__init__()
        if isinstance(args, string_types):
            self.value = args
        else:
            self.value = args[0] + args[1].value + args[2]


SimpleValue.grammar = some(SimpleValueUnit)


class SimpleRangeValue(LeafRule):
    """Match an unquoted range bound."""

    grammar = attr('value', re.compile(r"([^\s\)\(-]|-+[^\s\)\(>])+"))


class RangeValue(UnaryRule):
    """Match a range bound."""

    grammar = attr('op', [DoubleQuotedString, SimpleRangeValue])


class RangeOp(BinaryRule):
    """Match a range expression ``left->right``."""

    grammar = (
        attr('left', RangeValue),
        Literal('->'),
        attr('right', RangeValue)
    )


class Value(UnaryRule):
    """Match any kind of value."""

    grammar = attr('op', [
        RangeOp,
        SingleQuotedString,
        DoubleQuotedString,
        SlashQuotedString,
        SimpleValue,
    ])


class NestableKeyword(LeafRule):
    """Match keywords that accept a nested query."""

    grammar = attr('value', [
        re.compile('refersto', re.I),
        re.compile('citedby', re.I),
    ])


class Number(LeafRule):
    """Match an integer."""

    grammar = attr('value', re.compile(r'\d+'))


class ValueQuery(UnaryRule):
    """Match a query consisting of a value only."""

    grammar = attr('op', Value)


class Query(ListRule):
    """Match queries joined by boolean operators."""


class NotKeywordValue(LeafRule):
    """Match a value that is not a keyword."""


class KeywordQuery(BinaryRule):
    """Match a ``keyword:value`` query."""


class EmptyQueryRule(LeafRule):
    """Match an empty query."""

    grammar = attr('value', re.compile(r'\s*'))


KeywordQuery.grammar = [
    (
        attr('left', KeywordRule),
        omit(_, Literal(':'), _),
        attr('right', NestedKeywordsRule)
    ),
    (
        attr('left', KeywordRule),
        omit(Literal(':'), _),
        attr('right', Value)
    ),
    (
        attr('left', KeywordRule),
        omit(Literal(':'), _),
        attr('right', Query)
    ),
]


class SimpleQuery(UnaryRule):
    """Match a keyword query or a value query."""

    grammar = attr('op', [KeywordQuery, ValueQuery])


class ParenthesizedQuery(UnaryRule):
    """Match a query enclosed in parentheses."""

    grammar = (
        omit(Literal('('), _),
        attr('op', Query),
        omit(_, Literal(')')),
    )


class NotQuery(UnaryRule):
    """Match a negated query."""

    grammar = [
        (
            omit(Not),
            [
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('-')),
            attr('op', SimpleQuery),
        ),
    ]


class AndQuery(UnaryRule):
    """Match the right-hand side of an ``AND`` operation."""

    grammar = [
        (
            omit(And),
            [
                (omit(Whitespace), attr('op', NotQuery)),
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('+')),
            attr('op', SimpleQuery),
        ),
    ]


class ImplicitAndQuery(UnaryRule):
    """Match a query joined by an implicit ``AND``."""

    grammar = [
        attr('op', NotQuery),
        attr('op', ParenthesizedQuery),
        attr('op', SimpleQuery),
    ]


class OrQuery(UnaryRule):
    """Match the right-hand side of an ``OR`` operation."""

    grammar = [
        (
            omit(Or),
            [
                (omit(Whitespace), attr('op', NotQuery)),
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('|')),
            attr('op', SimpleQuery),
        ),
    ]


Query.grammar = attr('children', (
    [
        NotQuery,
        ParenthesizedQuery,
        SimpleQuery,
    ],
    maybe_some((
        omit(_),
        [
            AndQuery,
            OrQuery,
            ImplicitAndQuery,
        ]
    )),
))


class Main(UnaryRule):
    """Match a complete query."""

    initialized = False

    def __init__(self):
        """Initialize list of allowed keywords on first call."""
        if not Main.initialized:
            from invenio_query_parser.utils import build_valid_keywords_grammar
            build_valid_keywords_grammar()
            Main.initialized = True

    grammar = [
        (omit(_), attr('op', Query), omit(_)),
        attr('op', EmptyQueryRule),
    ]

# pylint: enable=C0321,R0903
