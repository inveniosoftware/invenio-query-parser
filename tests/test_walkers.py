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

"""Unit tests for the search engine query parsers."""

import pypeg2
from pytest import generate_tests

from invenio_query_parser.ast import GreaterOp, Keyword, KeywordOp, Value
from invenio_query_parser.contrib.elasticsearch.walkers import dsl
from invenio_query_parser.contrib.spires import converter
from invenio_query_parser.contrib.spires.walkers import spires_to_invenio
from invenio_query_parser.parser import Main
from invenio_query_parser.walkers import match_unit
from invenio_query_parser.walkers.pypeg_to_ast import PypegConverter


def generate_walker_test(query, expected):
    def func(self):
        tree = self.parser.parse_query(query)
        new_tree = tree.accept(self.walker())
        assert new_tree == expected
    return func


@generate_tests(generate_walker_test)  # pylint: disable=R0903
class TestSpiresToInvenio(object):
    """Test SPIRES parser functionality."""

    @classmethod
    def setup_class(cls):
        cls.walker = spires_to_invenio.SpiresToInvenio
        cls.parser = converter.SpiresToInvenioSyntaxConverter()

    queries = (
        ("find t quark",
         KeywordOp(Keyword('title'), Value('quark'))),
        ("find d after yesterday",
         KeywordOp(Keyword('year'), GreaterOp(Value('yesterday')))),
    )


def generate_dsl_test(query, data, expected):
    def func(self):
        tree = pypeg2.parse(query, self.parser, whitespace="")
        tree = tree.accept(PypegConverter())
        new_tree = tree.accept(self.walker(**data or {}))
        assert new_tree == expected
    return func


@generate_tests(generate_dsl_test)  # pylint: disable=R0903
class TestElasticsearchDSL(object):
    """Test Elasticsearch DSL converter."""

    @classmethod
    def setup_class(cls):
        cls.walker = dsl.ElasticSearchDSL
        cls.parser = Main

    keyword_to_fields = {None: ['_all'], 'foo': ['test1', 'test2']}

    queries = (
        # Empty query
        ('', None, {'match_all': {}}),
        # Value queries
        ('bar', None, {'multi_match': {
            'fields': ['_all'], 'query': 'bar'
        }}),
        ('\'foo bar\'', None, {'multi_match': {
            'fields': ['_all'],
            'query': 'foo bar',
            'type': 'phrase'
        }}),
        ('"foo bar"', None, {'term': {'_all': 'foo bar'}}),
        # Key-value queries
        ('foo:bar', dict(keyword_to_fields=keyword_to_fields),
         {'multi_match': {'fields': ['test1', 'test2'], 'query': 'bar'}}),
        ('foo:\'bar baz\'', dict(keyword_to_fields=keyword_to_fields), {
            'multi_match': {
                'fields': ['test1', 'test2'], 'query': 'bar baz',
                'type': 'phrase',
            }
        }),
        ('foo:"bar baz"', dict(keyword_to_fields=keyword_to_fields), {
            'bool': {'should': [
                {'term': {'test1': 'bar baz'}},
                {'term': {'test2': 'bar baz'}},
            ]}
        })
    )


def generate_match_unit_test(query, data, expected):
    def func(self):
        tree = pypeg2.parse(query, self.parser, whitespace="")
        tree = tree.accept(PypegConverter())
        new_tree = tree.accept(self.walker(data))
        assert new_tree == expected
    return func


@generate_tests(generate_match_unit_test)  # pylint: disable=R0903
class TestMatchUnit(object):
    """Test MatchUnit functionality."""

    @classmethod
    def setup_class(cls):
        cls.walker = match_unit.MatchUnit
        cls.parser = Main

    queries = (
        ('', None, True),

        # Value query
        ('test', {'data': 'test'}, True),
        ('/^test.*$/', {'data': 'test'}, True),
        ('/^test.*$/', {'data': 'testing'}, True),
        ('/^test.*$/', {'data': 'notest'}, False),
        ('test', {'data': ['bar', 'test']}, True),
        ('test', {'data': ['bar', 'baz']}, False),
        ('test', {'data': [{'name': 'bar'}, {'name': 'test'}]}, True),

        # Keyword query
        ('title:"Test"', {'title': 'Test'}, True),
        ('title:"Test"', {'title': 'NoTest'}, False),
        ('title:Test', {'title': 'My Testing'}, True),

        # Test list matching
        ('author:Ellis',
         {'author': [{'name': 'Higgs'}, {'name': 'Ellis'}]},
         True),

        # Range queries
        ('data:b->h', {'data': 'a'}, False),
        ('data:b->h', {'data': 'b'}, True),
        ('data:b->h', {'data': 'boo'}, True),
        ('data:b->h', {'data': 'f'}, True),
        ('data:b->h', {'data': 'foo'}, True),
        ('data:b->h', {'data': 'h'}, True),
        ('data:b->h', {'data': 'z'}, False),

        # Boolean operations
        ('title:"Test" AND data:\'foo bar\'',
         {'title': 'Test', 'data': 'foo bar'},
         True),
        ('title:"Test" AND NOT data:\'foo bar\'',
         {'title': 'Test', 'data': 'foo bar'},
         False),
        ('title:"Test" OR data:\'foo bar\'',
         {'title': 'Test', 'data': 'foo bar'},
         True),

    )
