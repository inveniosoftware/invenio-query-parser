# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Unit tests for the visitor decorator."""

from invenio_query_parser.visitor import make_visitor


class A(object):
    pass


class B(object):
    pass


class TestVisitor(object):
    visitor = make_visitor()

    @visitor(A)
    def visit(self, el):  # pylint: disable=W0613
        return 'A'

    @visitor(B)
    def visit(self, el):  # pylint: disable=W0613
        return 'B'

    def test_visit_a(self):
        assert self.visit(A()) == 'A'

    def test_visit_b(self):
        assert self.visit(B()) == 'B'


class TestVisitorInheritance(TestVisitor):
    visitor = make_visitor(TestVisitor.visitor)

    @visitor(B)
    def visit(self, el):
        return 'BB'

    def test_visit_a(self):
        assert self.visit(A()) == 'A'

    def test_visit_b(self):
        assert self.visit(B()) == 'BB'
