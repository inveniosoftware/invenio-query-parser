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

"""Unit tests for the search engine query parsers."""

import pypeg2

import pytest
from pytest import generate_tests

from invenio_query_parser.ast import GreaterOp, Keyword, KeywordOp, Value
from invenio_query_parser.contrib.elasticsearch.walkers import dsl
from invenio_query_parser.contrib.spires import converter
from invenio_query_parser.contrib.spires.walkers import spires_to_invenio
from invenio_query_parser.parser import Main
from invenio_query_parser.walkers import match_unit
from invenio_query_parser.walkers.pypeg_to_ast import PypegConverter
from invenio_query_parser.utils import build_valid_keywords_grammar


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
        build_valid_keywords_grammar()

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
        if type(expected) is type(BaseException):
            with pytest.raises(expected):
                new_tree = tree.accept(self.walker(**data or {}))
        else:
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
        build_valid_keywords_grammar()

    keyword_to_fields = {None: ['_all'], 'foo': ['test1', 'test2']}

    test_empty_query = (
        '',
        None,
        {'match_all': {}}
    )

    # Combined queries - boolean operators
    test_and_query = (
        'boo:bar baz',
        None,
        {"bool": {"must": [{"multi_match": {"fields": ["boo"], "query": "bar",
                                            }}, {"multi_match": {
                                                 "fields": ["_all"],
                                                 "query": "baz", }}]}}
    )

    test_or_query = (
        'boo:bar OR baz',
        None,
        {"bool": {"should": [{"multi_match": {"fields": ["boo"],
                                              "query": "bar", }},
                             {"multi_match": {"fields": ["_all"],
                              "query": "baz", }}]}},
    )

    test_not_query = (
        'boo:bar AND NOT boo:bar',
        None,
        {"bool": {"must":
                  [{"multi_match":
                    {"fields": ["boo"], "query": "bar"}},
                   {"bool": {"must_not":
                             [{"multi_match": {"fields": ["boo"],
                              "query": "bar"}}]}}]}}
    )

    left = {"multi_match": {"fields": ["_all"], "query": "ddd"}}
    right_right = {"bool": {"must": [{"multi_match": {"fields": ["_all"],
                            "query": "aaa"}},
                                     {"multi_match": {"fields": ["_all"],
                                      "query": "bbb"}}]}}
    right_left = {"bool": {"must_not": [{"multi_match": {"fields": ["_all"],
                  "query": "ccc"}}]}}
    right = {"bool": {"must": [right_right, right_left]}}

    test_combined_bool_query = (
        '((aaa AND bbb) AND NOT ccc) OR ddd',
        None,
        {"bool": {"should": [right, left]}}
    )

    # Operators
    test_greater_op = (
        'date:1984<',
        None,
        {"range": {"date": {"gt": "1984"}}}
    )

    test_lower_op = (
        'year:1984>',
        None,
        {"range": {"year": {"lt": "1984"}}}
    )

    test_gte_op = (
        'year:1984<=',
        None,
        {"range": {"year": {"gte": "1984"}}}
    )

    test_lte_op = (
        'year:1984>=',
        None,
        {"range": {"year": {"lte": "1984"}}}
    )
    test_range_op = (
        'year:2000->2012',
        None,
        {"range": {"year": {"gte": "2000", "lte": "2012"}}}
    )

    test_multiple_range_op = (
        'foo:bar->baz',
        dict(keyword_to_fields=keyword_to_fields),
        {"bool": {
            "should": [
                {
                    "range": {
                        "test1": {
                            "gte": "bar",
                            "lte": "baz"
                        }
                    }
                },
                {
                    "range": {
                        "test2": {
                            "gte": "bar",
                            "lte": "baz"
                        }
                    }
                }
            ]
        }}
    )

    test_keyword_with_regex = (
        'title: /bar/',
        None,
        {"regexp": {"title": "bar"}}
    )

    test_keywords_with_regex = (
        'foo: /bar/',
        dict(keyword_to_fields=keyword_to_fields),
        {
            "bool": {
                "should": [
                    {
                        "regexp": {
                            "test1": "bar"
                        }
                    },
                    {
                        "regexp": {
                            "test2": "bar"
                        }
                    }
                ]
            }
        })

    test_regex_for_all_should_fail = (
        '/bar/',
        None,
        RuntimeError
    )

    test_keywords_to_fields = (
        'foo: bar',
        dict(keyword_to_fields={'foo': {'a': ['test1', 'test2']}}),
        {'multi_match': {'fields': ['test1', 'test2'], 'query': 'bar'}}
    )

    queries = (
        test_empty_query,
        # Value queries
        ('bar', None, {'multi_match': {
            'fields': ['_all'], 'query': 'bar'
        }}),
        ('\'foo bar\'', None, {'multi_match': {
            'fields': ['_all'],
            'query': 'foo bar',
            'type': 'phrase'
        }}),
        ('"foo bar"', None, {
            'multi_match': {
                'fields': ['_all'], 'query': 'foo bar', 'type': 'phrase',
            }
        }),
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
            'multi_match': {
                'fields': ['test1', 'test2'], 'query': 'bar baz',
                'type': 'phrase',
            }
        }),
        test_and_query,
        test_or_query,
        test_not_query,
        test_combined_bool_query,
        # test_greater_op, Issue inveniosoftware/invenio-query-parser#43
        # test_lower_op,
        # test_gte_op,
        # test_lte_op,
        test_range_op,
        test_multiple_range_op,
        test_keyword_with_regex,
        test_keywords_with_regex,
        test_regex_for_all_should_fail,
        test_keywords_to_fields
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
        build_valid_keywords_grammar()

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
        ('test', {'data': ({'name': 'bar'}, {'name': 'test'})}, True),

        # Keyword query
        ('title:"Test"', {'title': 'Test'}, True),
        ('title:"Test"', {'title': 'NoTest'}, False),
        ('title:Test', {'title': 'My Testing'}, True),
        ('non_existing:Test', {'title': 'My Testing'}, False),

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
