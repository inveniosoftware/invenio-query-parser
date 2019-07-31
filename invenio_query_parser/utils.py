# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions for building list of allowed keywords."""

from __future__ import absolute_import, print_function

import re

import pkg_resources
from pypeg2 import attr


def build_valid_keywords_grammar(keywords=None):
    """Update parser grammar to add a list of allowed keywords."""
    from invenio_query_parser.parser import KeywordQuery, KeywordRule, \
        NotKeywordValue, SimpleQuery, ValueQuery

    if keywords:
        KeywordRule.grammar = attr('value', re.compile(
            r"(\d\d\d\w{{0,3}}|{0})\b".format("|".join(keywords), re.I)))

        NotKeywordValue.grammar = attr('value', re.compile(
            r'\b(?!\d\d\d\w{{0,3}}|{0}:)\S+\b:'.format(
                ":|".join(keywords))))

        SimpleQuery.grammar = attr(
            'op', [NotKeywordValue, KeywordQuery, ValueQuery])
    else:
        KeywordRule.grammar = attr('value', re.compile(r"[\w\d]+(\.[\w\d]+)*"))
        SimpleQuery.grammar = attr('op', [KeywordQuery, ValueQuery])
