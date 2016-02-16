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

    def __init__(self):
        pass


class UnaryRule(ast.UnaryOp):

    def __init__(self):
        pass


class BinaryRule(ast.BinaryOp):

    def __init__(self):
        pass


class ListRule(ast.ListOp):

    def __init__(self):
        pass


class Whitespace(LeafRule):
    grammar = attr('value', re.compile(r"\s+"))


_ = optional(Whitespace)


class Not(object):
    grammar = omit([
        omit(re.compile(r"AND\s+NOT")),
        re.compile(r"NOT"),
        Literal('-'),
    ])


class And(object):
    grammar = omit([
        re.compile(r"AND"),
        Literal('+'),
    ])


class Or(object):
    grammar = omit([
        re.compile(r"OR"),
        Literal('|'),
    ])


class KeywordRule(LeafRule):
    grammar = attr('value', re.compile(r"[\w\d]+(\.[\w\d]+)*"))


class NestedKeywordsRule(LeafRule):
    grammar = attr('value', re.compile(
        r"(([\w\d]+(\.[\w\d]+)*):\s*)+([\w\d]+(\.[\w\d]+)*)"))


class SingleQuotedString(LeafRule):
    grammar = Literal("'"), attr('value', re.compile(r"([^']|\\.)*")), \
        Literal("'")


class DoubleQuotedString(LeafRule):
    grammar = Literal('"'), attr('value', re.compile(r'([^"]|\\.)*')), \
        Literal('"')


class SlashQuotedString(LeafRule):
    grammar = Literal('/'), attr('value', re.compile(r"([^/]|\\.)*")), \
        Literal('/')


class SimpleValue(LeafRule):

    def __init__(self, values):
        super(SimpleValue, self).__init__()
        self.value = "".join(v.value for v in values)


class SimpleValueUnit(LeafRule):
    grammar = [
        re.compile(r"[^\s\)\(:]+"),
        (re.compile(r'\('), SimpleValue, re.compile(r'\)')),
    ]

    def __init__(self, args):
        super(SimpleValueUnit, self).__init__()
        if isinstance(args, string_types):
            self.value = args
        else:
            self.value = args[0] + args[1].value + args[2]


SimpleValue.grammar = some(SimpleValueUnit)


class SimpleRangeValue(LeafRule):
    grammar = attr('value', re.compile(r"([^\s\)\(-]|-+[^\s\)\(>])+"))


class RangeValue(UnaryRule):
    grammar = attr('op', [DoubleQuotedString, SimpleRangeValue])


class RangeOp(BinaryRule):
    grammar = (
        attr('left', RangeValue),
        Literal('->'),
        attr('right', RangeValue)
    )


class Value(UnaryRule):
    grammar = attr('op', [
        RangeOp,
        SingleQuotedString,
        DoubleQuotedString,
        SlashQuotedString,
        SimpleValue,
    ])


class NestableKeyword(LeafRule):
    grammar = attr('value', [
        re.compile('refersto', re.I),
        re.compile('citedby', re.I),
    ])


class Number(LeafRule):
    grammar = attr('value', re.compile(r'\d+'))


class ValueQuery(UnaryRule):
    grammar = attr('op', Value)


class Query(ListRule):
    pass


class NotKeywordValue(LeafRule):
    pass


class KeywordQuery(BinaryRule):
    pass


class EmptyQueryRule(LeafRule):
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
    grammar = attr('op', [KeywordQuery, ValueQuery])


class ParenthesizedQuery(UnaryRule):
    grammar = (
        omit(Literal('('), _),
        attr('op', Query),
        omit(_, Literal(')')),
    )


class NotQuery(UnaryRule):
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
    grammar = [
        attr('op', NotQuery),
        attr('op', ParenthesizedQuery),
        attr('op', SimpleQuery),
    ]


class OrQuery(UnaryRule):
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
