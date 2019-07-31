# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
