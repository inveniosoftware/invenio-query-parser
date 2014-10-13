# Abstract classes


class BinaryOp(object):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit(self,
                             self.left.accept(visitor),
                             self.right.accept(visitor))

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.left == other.left
                and self.right == other.right)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__,
                               repr(self.left), repr(self.right))


class UnaryOp(object):

    def __init__(self, op):
        self.op = op

    def accept(self, visitor):
        return visitor.visit(self, self.op.accept(visitor))

    def __eq__(self, other):
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.op))


class ListOp(object):

    def __init__(self, children):
        try:
            iter(children)
        except TypeError:
            self.children = [children]
        else:
            self.children = children

    def accept(self, visitor):
        return visitor.visit(self, [c.accept(visitor) for c in self.children])

    def __eq__(self, other):
        return type(self) == type(other) and self.op == other.op

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.children))


class Leaf(object):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))


# Concrete classes

class BinaryKeywordBase(BinaryOp):
    @property
    def keyword(self):
        if self.left:
            if isinstance(self.left, SpiresOp):
                return self.left.keyword
        elif isinstance(self.right, SpiresOp):
            return self.right.keyword
        return None


class AndOp(BinaryKeywordBase):
    pass


class OrOp(BinaryKeywordBase):
    pass


class NotOp(UnaryOp):
    @property
    def keyword(self):
        return getattr(self.op, 'keyword')


class RangeOp(BinaryOp):
    pass


class LowerOp(UnaryOp):
    pass


class LowerEqualOp(UnaryOp):
    pass


class GreaterOp(UnaryOp):
    pass


class GreaterEqualOp(UnaryOp):
    pass


class KeywordOp(BinaryOp):
    pass


class SpiresOp(BinaryOp):
    @property
    def keyword(self):
        return self.left


class ValueQuery(UnaryOp):
    pass


class Keyword(Leaf):
    pass


class Value(Leaf):
    pass


class SingleQuotedValue(Leaf):
    pass


class DoubleQuotedValue(Leaf):
    pass


class RegexValue(Leaf):
    pass


class EmptyQuery(Leaf):
    pass
