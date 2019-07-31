# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import shutil
import tempfile

import pytest


def generate_tests(generate_test):
    def fun(cls):
        for count, args in enumerate(cls.queries):
            func = generate_test(*args)
            func.__name__ = 'test_%s' % count
            func.__doc__ = "Parsing query %s" % args[0]
            setattr(cls, func.__name__, func)
        return cls
    return fun


def pytest_configure():
    pytest.generate_tests = generate_tests
