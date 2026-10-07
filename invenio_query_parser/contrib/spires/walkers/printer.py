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

"""SPIRES extended repr printer."""

from invenio_query_parser.visitor import make_visitor
from invenio_query_parser.walkers import printer

from .. import parser
from ..ast import SpiresOp


class TreePrinter(printer.TreePrinter):
    """Print an AST with SPIRES operations as a query."""

    visitor = make_visitor(printer.TreePrinter.visitor)

    @visitor(SpiresOp)
    def visit(self, node, left, right):
        """Print ``SpiresOp`` node as query string."""
        return "find %s %s" % (left, right)
