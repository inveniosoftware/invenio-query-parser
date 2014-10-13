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
