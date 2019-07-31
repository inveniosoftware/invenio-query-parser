# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Implement AST vistor."""

import re
from collections import MutableMapping, Sequence

import six

from invenio_query_parser.ast import AndOp, DoubleQuotedValue, EmptyQuery, \
    Keyword, KeywordOp, NotOp, OrOp, RangeOp, RegexValue, SingleQuotedValue, \
    Value, ValueQuery
from invenio_query_parser.visitor import make_visitor


def dottable_getitem(data, dottable_key, default=None):
    """Return item as ``dict.__getitem__` but using keys with dots.

    It does not address indexes in iterables.
    """
    def getitem(value, *keys):
        if not keys:
            return default
        elif len(keys) == 1:
            key = keys[0]
            if isinstance(value, MutableMapping):
                return value.get(key, default)
            elif isinstance(value, Sequence) and \
                    not isinstance(value, six.string_types):
                return [getitem(v, key) for v in value]
            return default
        return getitem(getitem(value, keys[0]), *keys[1:])
    return getitem(data, *dottable_key.split('.'))


def match_unit(data, p, m='a'):
    """Match data to basic match unit."""
    if data is None:
        return p is None

    # compile search value only once for non exact search
    if m != 'e' and isinstance(p, six.string_types):
        p = re.compile(p)

    if isinstance(data, Sequence) and not isinstance(data, six.string_types):
        return any([match_unit(field, p, m=m)
                    for field in data])
    elif isinstance(data, MutableMapping):
        return any([match_unit(field, p, m=m)
                    for field in data.values()])

    # Inclusive range query
    if isinstance(p, tuple):
        left, right = p
        return (left <= data) and (data <= right)

    if m == 'e':
        return six.text_type(data) == p
    return p.search(six.text_type(data)) is not None


class MatchUnit(object):
    """Implement visitor using ``match_unit`` API."""

    visitor = make_visitor()

    def __init__(self, data, getitem=dottable_getitem):
        """Initialize matching unit with data and keyword value getter."""
        self.data = data
        self.getitem = getitem

    # pylint: disable=W0613,E0102

    @visitor(AndOp)
    def visit(self, node, left, right):
        return left & right

    @visitor(OrOp)
    def visit(self, node, left, right):
        return left | right

    @visitor(NotOp)
    def visit(self, node, op):
        return not op

    @visitor(KeywordOp)
    def visit(self, node, left, right):
        return match_unit(self.getitem(self.data, left), **right)

    @visitor(ValueQuery)
    def visit(self, node, op):
        return match_unit(self.data, **op)

    @visitor(Keyword)
    def visit(self, node):
        return node.value

    @visitor(Value)
    def visit(self, node):
        return dict(p=node.value)

    @visitor(SingleQuotedValue)
    def visit(self, node):
        return dict(p=node.value, m='p')

    @visitor(DoubleQuotedValue)
    def visit(self, node):
        return dict(p=node.value, m='e')

    @visitor(RegexValue)
    def visit(self, node):
        return dict(p=node.value, m='r')

    @visitor(RangeOp)
    def visit(self, node, left, right):
        return dict(p=(left['p'], right['p']))

    @visitor(EmptyQuery)
    def visit(self, node):
        return True

    # pylint: enable=W0612,E0102
