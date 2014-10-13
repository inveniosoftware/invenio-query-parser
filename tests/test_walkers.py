"""Unit tests for the search engine query parsers."""

from pytest import generate_tests

from invenio_query_parser import SpiresToInvenioSyntaxConverter, load_walkers
from invenio_query_parser.ast import KeywordOp, Keyword, Value, GreaterOp


def generate_walker_test(query, expected):
    def func(self):
        tree = self.parser.parse_query(query)
        new_tree = tree.accept(self.walker())
        assert new_tree == expected
    return func


@generate_tests(generate_walker_test)  # pylint: disable=R0903
class TestSpiresToInvenio(object):
    """Test parser functionality"""

    @classmethod
    def setup_class(cls):
        cls.walker = load_walkers().SpiresToInvenio
        cls.parser = SpiresToInvenioSyntaxConverter()

    queries = (
        ("find t quark",
         KeywordOp(Keyword('title'), Value('quark'))),
        ("find d after yesterday",
         KeywordOp(Keyword('year'), GreaterOp(Value('yesterday')))),
    )
