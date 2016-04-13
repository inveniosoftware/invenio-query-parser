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
