# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SPIRES extended repr printer."""

from invenio_query_parser.visitor import make_visitor
from invenio_query_parser.walkers import printer

from .. import parser
from ..ast import SpiresOp


class TreePrinter(printer.TreePrinter):
    visitor = make_visitor(repr_printer.TreePrinter.visitor)

    @visitor(SpiresOp)
    def visit(self, node, left, right):
        return "find %s %s" % (left, right)
