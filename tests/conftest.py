# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014, 2016 CERN.
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

import pytest
import shutil
import tempfile

from flask import Flask


def generate_tests(generate_test):
    def fun(cls):
        for count, args in enumerate(cls.queries):
            func = generate_test(*args)
            func.__name__ = 'test_%s' % count
            func.__doc__ = "Parsing query %s" % args[0]
            setattr(cls, func.__name__, func)
        return cls
    return fun


def pytest_namespace():
    return dict((
        ("generate_tests", generate_tests),
    ))


@pytest.fixture()
def app(request):
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()
    app = Flask(__name__, instance_path=instance_path)
    app.config.update(
        SEARCH_ALLOWED_KEYWORDS=set([
            'title', 'author']),
        TESTING=True,
    )

    def teardown():
        shutil.rmtree(instance_path)
    request.addfinalizer(teardown)

    return app
