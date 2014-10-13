from invenio_query_parser.visitor import make_visitor
from invenio_query_parser import ast
from invenio_query_parser import parser


class PypegConverter(object):
    visitor = make_visitor()

    # pylint: disable=W0613,E0102

    @visitor(parser.Whitespace)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.Not)
    def visit(self, node, child):
        return ast.NotOp(child)

    @visitor(parser.And)
    def visit(self, node, left, right):
        return ast.AndOp(left, right)

    @visitor(parser.Or)
    def visit(self, node, left, right):
        return ast.Or(left, right)

    @visitor(parser.KeywordRule)
    def visit(self, node):
        return ast.Keyword(node.value)

    @visitor(parser.SpiresKeywordRule)
    def visit(self, node):
        return ast.Keyword(node.value)

    @visitor(parser.SingleQuotedString)
    def visit(self, node):
        return ast.SingleQuotedValue(node.value)

    @visitor(parser.DoubleQuotedString)
    def visit(self, node):
        return ast.DoubleQuotedValue(node.value)

    @visitor(parser.SlashQuotedString)
    def visit(self, node):
        return ast.RegexValue(node.value)

    @visitor(parser.SimpleValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.SimpleRangeValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.RangeValue)
    def visit(self, node, child):
        return child

    @visitor(parser.RangeOp)
    def visit(self, node, left, right):
        return ast.RangeOp(left, right)

    @visitor(parser.GreaterQuery)
    def visit(self, node, child):
        return ast.GreaterOp(child)

    @visitor(parser.GreaterEqualQuery)
    def visit(self, node, child):
        return ast.GreaterEqualOp(child)

    @visitor(parser.LowerQuery)
    def visit(self, node, child):
        return ast.LowerOp(child)

    @visitor(parser.LowerEqualQuery)
    def visit(self, node, child):
        return ast.LowerEqualOp(child)

    @visitor(parser.Number)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.Value)
    def visit(self, node, child):
        return child

    @visitor(parser.NestableKeyword)
    def visit(self, node):
        return ast.Keyword(node.value)

    @visitor(parser.SpiresSimpleValue)
    def visit(self, node):
        return ast.Value(node.value)

    @visitor(parser.SpiresValue)
    def visit(self, node, children):
        return ast.Value("".join([c.value for c in children]))

    @visitor(parser.SpiresValueQuery)
    def visit(self, node, child):
        return ast.ValueQuery(child)

    @visitor(parser.SpiresSimpleQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.SpiresParenthesizedQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.SpiresNotQuery)
    def visit(self, node, child):
        return ast.AndOp(None, ast.NotOp(child))

    @visitor(parser.SpiresAndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(parser.SpiresOrQuery)
    def visit(self, node, child):
        return ast.OrOp(None, child)

    @visitor(parser.ValueQuery)
    def visit(self, node, child):
        return ast.ValueQuery(child)

    @visitor(parser.SpiresKeywordQuery)
    def visit(self, node, keyword, value):
        return ast.SpiresOp(keyword, value)

    @visitor(parser.KeywordQuery)
    def visit(self, node, keyword, value):
        return ast.KeywordOp(keyword, value)

    @visitor(parser.SimpleQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.ParenthesizedQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.NotQuery)
    def visit(self, node, child):
        return ast.AndOp(None, ast.NotOp(child))

    @visitor(parser.AndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(parser.ImplicitAndQuery)
    def visit(self, node, child):
        return ast.AndOp(None, child)

    @visitor(parser.OrQuery)
    def visit(self, node, child):
        return ast.OrOp(None, child)

    @visitor(parser.Query)
    def visit(self, node, children):
        # Build the boolean expression, left to right
        # x and y or z and ... --> ((x and y) or z) and ...
        tree = children[0]
        for booleanNode in children[1:]:
            booleanNode.left = tree
            tree = booleanNode
        return tree

    @visitor(parser.SpiresQuery)
    def visit(self, node, children):
        # Assign implicit keyword
        # find author x and y --> find author x and author y

        def assign_implicit_keyword(implicit_keyword, node):
            """
            Note: this function has side effects on node content
            """
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.ValueQuery:
                node.right = ast.SpiresOp(implicit_keyword, node.right.op)
            if type(node) in [ast.AndOp, ast.OrOp] and \
               type(node.right) == ast.NotOp:
                assign_implicit_keyword(implicit_keyword, node.right)
            if type(node) in [ast.NotOp] and \
               type(node.op) == ast.ValueQuery:
                node.op = ast.SpiresOp(implicit_keyword, node.op.op)

        implicit_keyword = None
        for child in children:
            new_keyword = getattr(child, 'keyword', None)
            if new_keyword is not None:
                implicit_keyword = new_keyword
            if implicit_keyword is not None:
                assign_implicit_keyword(implicit_keyword, child)

        # Build the boolean expression, left to right
        # x and y or z and ... --> ((x and y) or z) and ...
        tree = children[0]
        for booleanNode in children[1:]:
            booleanNode.left = tree
            tree = booleanNode
        return tree

    @visitor(parser.FindQuery)
    def visit(self, node, child):
        return child

    @visitor(parser.EmptyQueryRule)
    def visit(self, node):
        return ast.EmptyQuery(node.value)

    @visitor(parser.Main)
    def visit(self, node, child):
        return child

    # pylint: enable=W0612,E0102
