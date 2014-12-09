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

from pytest import generate_tests

from invenio_query_parser.contrib.spires.walkers import spires_to_invenio
from invenio_query_parser.contrib.spires import converter
from invenio_query_parser.ast import KeywordOp, Keyword, Value, GreaterOp


def generate_walker_test(query, expected):
    def func(self):
        tree = self.parser.parse_query(query)
        new_tree = tree.accept(self.walker())
        assert new_tree == expected
    return func


@generate_tests(generate_walker_test)  # pylint: disable=R0903
class TestSpiresToInvenio(object):

    """Test parser functionality."""

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
