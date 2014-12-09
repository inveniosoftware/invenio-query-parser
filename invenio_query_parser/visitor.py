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

"""Store the actual visitor methods."""


class make_visitor(object):
    """Make a visitor decorator."""

    def __init__(self, methods=None):
        self._methods = {}
        self.methods = methods or {}

    def __getitem__(self, key):
        if key in self._methods:
            return self._methods[key]
        return self.methods[key]

    def __setitem__(self, key, value):
        self._methods[key] = value

    # The actual @visitor decorator
    def __call__(self, arg_type):
        """Decorator that creates a visitor method."""

        # Delegating visitor implementation

        def _visitor_impl(new_self, arg, *args, **kwargs):
            """Actual visitor method implementation."""
            method = self[type(arg)]
            return method(new_self, arg, *args, **kwargs)

        def decorator(fn):
            self[arg_type] = fn
            # Replace all decorated methods with _visitor_impl
            return _visitor_impl

        return decorator
