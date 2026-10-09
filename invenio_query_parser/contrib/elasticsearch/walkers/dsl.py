# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2015, 2016 CERN.
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

"""Implement AST convertor to search engine DSL.

The DSL module is provided by :mod:`invenio_search.api`, so it works with
whichever search backend (Elasticsearch or OpenSearch) is installed.
"""

from functools import reduce
from operator import and_, or_

from invenio_search.api import dsl

from invenio_query_parser.ast import AndOp, DoubleQuotedValue, EmptyQuery, \
    GreaterEqualOp, GreaterOp, Keyword, KeywordOp, LowerEqualOp, LowerOp, \
    NotOp, OrOp, RangeOp, RegexValue, SingleQuotedValue, Value, ValueQuery
from invenio_query_parser.visitor import make_visitor


class ElasticSearchDSL(object):
    """Implement visitor to create search engine DSL queries."""

    visitor = make_visitor()

    def __init__(self, keyword_to_fields=None):
        """Provide a dictinary mapping from keywords to search field(s)."""
        self.keyword_to_fields = keyword_to_fields or {None: ['_all']}

    def get_fields_for_keyword(self, keyword, mode='a'):
        """Convert keyword to fields."""
        field = self.keyword_to_fields.get(keyword, keyword)
        if isinstance(field, dict):
            return field[mode]
        elif isinstance(field, (list, tuple)):
            return field
        return [field]

    # pylint: disable=W0613,E0102

    @visitor(AndOp)
    def visit(self, node, left, right):
        """Build search DSL for ``AndOp`` node."""
        return left & right

    @visitor(OrOp)
    def visit(self, node, left, right):
        """Build search DSL for ``OrOp`` node."""
        return left | right

    @visitor(NotOp)
    def visit(self, node, op):
        """Build search DSL for ``NotOp`` node."""
        return ~op

    @visitor(KeywordOp)
    def visit(self, node, left, right):
        """Build search DSL for ``KeywordOp`` node."""
        if callable(right):
            return right(left)
        raise RuntimeError('Not supported second level operation.')

    @visitor(ValueQuery)
    def visit(self, node, op):
        """Build search DSL for ``ValueQuery`` node."""
        return op(None)

    @visitor(Keyword)
    def visit(self, node):
        """Build search DSL for ``Keyword`` node."""
        return node.value

    @visitor(Value)
    def visit(self, node):
        """Build search DSL for ``Value`` node."""
        def query(keyword):
            fields = self.get_fields_for_keyword(keyword, mode='a')
            return dsl.Q('multi_match', query=node.value, fields=fields)
        return query

    @visitor(SingleQuotedValue)
    def visit(self, node):
        """Build search DSL for ``SingleQuotedValue`` node."""
        def query(keyword):
            fields = self.get_fields_for_keyword(keyword, mode='p')
            return dsl.Q('multi_match', query=node.value, fields=fields,
                         type='phrase')
        return query

    @visitor(DoubleQuotedValue)
    def visit(self, node):
        """Build search DSL for ``DoubleQuotedValue`` node."""
        def query(keyword):
            fields = self.get_fields_for_keyword(keyword, mode='p')
            return dsl.Q('multi_match', query=node.value, fields=fields,
                         type='phrase')
        return query

    @visitor(RegexValue)
    def visit(self, node):
        """Build search DSL for ``RegexValue`` node."""
        def query(keyword):
            fields = self.get_fields_for_keyword(keyword, mode='r')
            if keyword is None or fields is None:
                raise RuntimeError('Not supported regex search for all fields')
            return reduce(or_, [
                dsl.Q('regexp', **{k: node.value}) for k in fields
            ])
        return query

    @visitor(EmptyQuery)
    def visit(self, node):
        """Build search DSL for ``EmptyQuery`` node."""
        return dsl.Q('match_all')

    def _range_operators(self, node, condition):
        def query(keyword):
            fields = self.get_fields_for_keyword(keyword, mode='r')
            return reduce(or_, [
                dsl.Q('range', **{k: condition}) for k in fields
            ])
        return query

    @visitor(RangeOp)
    def visit(self, node, left, right):
        """Build search DSL for ``RangeOp`` node."""
        condition = {}
        if left:
            condition['gte'] = left(None).to_dict()['multi_match']['query']
        if right:
            condition['lte'] = right(None).to_dict()['multi_match']['query']

        return self._range_operators(node, condition)

    @visitor(GreaterOp)
    def visit(self, node, value_fn):
        """Build search DSL for ``GreaterOp`` node."""
        condition = {'gt': value_fn(None).to_dict()['multi_match']['query']}
        return self._range_operators(node, condition)

    @visitor(LowerOp)
    def visit(self, node, value_fn):
        """Build search DSL for ``LowerOp`` node."""
        condition = {'lt': value_fn(None).to_dict()['multi_match']['query']}
        return self._range_operators(node, condition)

    @visitor(GreaterEqualOp)
    def visit(self, node, value_fn):
        """Build search DSL for ``GreaterEqualOp`` node."""
        condition = {'gte': value_fn(None).to_dict()['multi_match']['query']}
        return self._range_operators(node, condition)

    @visitor(LowerEqualOp)
    def visit(self, node, value_fn):
        """Build search DSL for ``LowerEqualOp`` node."""
        condition = {'lte': value_fn(None).to_dict()['multi_match']['query']}
        return self._range_operators(node, condition)

    # pylint: enable=W0612,E0102
