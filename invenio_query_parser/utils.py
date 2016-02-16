# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2016 CERN.
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

"""Utility functions for building list of allowed keywords."""

from __future__ import absolute_import, print_function

import re

import pkg_resources
from pypeg2 import attr


def build_valid_keywords_grammar():
    """Update parser grammar to add a list of allowed keywords."""
    try:
        pkg_resources.get_distribution('flask')
        from flask import current_app
        keywords_list = current_app.config.get('SEARCH_ALLOWED_KEYWORDS', [])
    except (pkg_resources.DistributionNotFound, RuntimeError):
        HAS_KEYWORDS = False
    else:
        HAS_KEYWORDS = True if keywords_list else False

    from invenio_query_parser.parser import KeywordQuery, KeywordRule, \
        NotKeywordValue, SimpleQuery, ValueQuery

    if HAS_KEYWORDS:
        KeywordRule.grammar = attr('value', re.compile(
            r"(\d\d\d\w{{0,3}}|{0})\b".format("|".join(keywords_list), re.I)))

        NotKeywordValue.grammar = attr('value', re.compile(
            r'\b(?!\d\d\d\w{{0,3}}|{0}:)\S+\b:'.format(
                ":|".join(keywords_list))))

        SimpleQuery.grammar = attr(
            'op', [NotKeywordValue, KeywordQuery, ValueQuery])
    else:
        KeywordRule.grammar = attr('value', re.compile(r"[\w\d]+(\.[\w\d]+)*"))
        SimpleQuery.grammar = attr('op', [KeywordQuery, ValueQuery])
