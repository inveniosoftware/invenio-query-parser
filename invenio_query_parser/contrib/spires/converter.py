# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SPIRES to Invenio query converter."""

import pypeg2

from invenio_query_parser.walkers import repr_printer

from .parser import Main
from .walkers import pypeg_to_ast


class SpiresToInvenioSyntaxConverter(object):
    def __init__(self):
        self.converter = pypeg_to_ast.PypegConverter()
        self.printer = repr_printer.TreeRepr()

    def parse_query(self, query):
        """Parse query string using given grammar"""
        tree = pypeg2.parse(query, Main, whitespace="")
        return tree.accept(self.converter)

    def convert_query(self, query):
        return self.parse_query(query).accept(self.printer)
