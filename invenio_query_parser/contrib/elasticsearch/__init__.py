# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Implement query convertor to Elastic Search DSL."""

import pypeg2

from invenio_query_parser.walkers.pypeg_to_ast import PypegConverter
from invenio_query_parser.parser import Main

from .walkers.dsl import ElasticSearchDSL


def invenio_query_factory(parser=None, walkers=None):
    """Create a parser returning Elastic Search DSL query instance."""
    parser = parser or Main
    walkers = walkers or [PypegConverter()]
    walkers.append(ElasticSearchDSL())

    def invenio_query(pattern):
        query = pypeg2.parse(pattern, parser, whitespace="")
        for walker in walkers:
            query = query.accept(walker)
        return query
    return invenio_query


IQ = invenio_query_factory()

__all__ = ('IQ', 'invenio_query_factory')
