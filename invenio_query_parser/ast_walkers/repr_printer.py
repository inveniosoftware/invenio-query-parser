from invenio_query_parser.visitor import make_visitor

from invenio_query_parser.ast import (AndOp, KeywordOp, OrOp,
                                      NotOp, Keyword, Value,
                                      SingleQuotedValue,
                                      DoubleQuotedValue, ValueQuery,
                                      RegexValue, RangeOp, SpiresOp,
                                      GreaterOp, GreaterEqualOp,
                                      LowerOp, LowerEqualOp, EmptyQuery)


class TreeRepr(object):
    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(AndOp)
    def visit(self, node, left, right):
        return '(%s and %s)' % (left, right)

    @visitor(OrOp)
    def visit(self, node, left, right):
        return '(%s or %s)' % (left, right)

    @visitor(NotOp)
    def visit(self, node, op):
        return '(not %s)' % op

    @visitor(KeywordOp)
    def visit(self, node, left, right):
        return '%s:%s' % (left, right)

    @visitor(Keyword)
    def visit(self, node):
        return '`%s`' % node.value

    @visitor(Value)
    def visit(self, node):
        return "'%s'" % node.value

    @visitor(ValueQuery)
    def visit(self, node, query):
        return query

    @visitor(SingleQuotedValue)
    def visit(self, node):
        return "'%s'" % node.value

    @visitor(DoubleQuotedValue)
    def visit(self, node):
        return '"%s"' % node.value

    @visitor(RegexValue)
    def visit(self, node):
        return "/%s/" % node.value

    @visitor(RangeOp)
    def visit(self, node, left, right):
        return "%s->%s" % (left, right)

    @visitor(SpiresOp)
    def visit(self, node, left, right):
        return "find %s %s" % (left, right)

    @visitor(GreaterOp)
    def visit(self, node, op):
        return '> %s' % op

    @visitor(GreaterEqualOp)
    def visit(self, node, op):
        return '>= %s' % op

    @visitor(LowerOp)
    def visit(self, node, op):
        return '< %s' % op

    @visitor(LowerEqualOp)
    def visit(self, node, op):
        return '<= %s' % op

    @visitor(EmptyQuery)
    def visit(self, node):
        return '__empty__'

    # pylint: enable=W0612,E0102
