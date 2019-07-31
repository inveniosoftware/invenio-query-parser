# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Define abstract SPIRES classes."""

from invenio_query_parser.ast import BinaryOp


class SpiresOp(BinaryOp):
    @property
    def keyword(self):
        return self.left
