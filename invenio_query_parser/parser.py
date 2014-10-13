import re

import pypeg2
from pypeg2 import (Keyword, maybe_some, optional, attr,
                    Literal, omit, some)

from invenio_query_parser import ast

SPIRES_KEYWORDS = {
# address
'address': 'address',
# affiliation
'affiliation': 'affiliation',
'affil': 'affiliation',
'aff': 'affiliation',
'af': 'affiliation',
'institution': 'affiliation',
'inst': 'affiliation',
# any field
'anyfield': 'anyfield',
'any': 'anyfield',
# author count
'authorcount': 'authorcount',
'ac': 'authorcount',
# citation / reference
'reference': 'reference',
'c': 'refersto',
'citation': 'reference',
'citedby': 'citedby',
'jour-vol-page': 'reference',
'jvp': 'reference',
# collaboration
'collaboration': 'collaboration',
'collab-name': 'collaboration',
'cn': 'collaboration',
# conference number
'confnumber': 'confnumber',
'conf-number': 'confnumber',
'cnum': 'confnumber',
# country
'country': 'country',
'cc': 'country',
# date
'date': 'year',
'd': 'year',
# date added
'date-added': 'datecreated',
'dadd': 'datecreated',
'da': 'datecreated',
# date updated
'date-updated': 'datemodified',
'dupd': 'datemodified',
'du': 'datemodified',
# first author
'firstauthor': 'firstauthor',
'first-author': 'firstauthor',
'fa': 'firstauthor',
# author
'author': 'author',
'a': 'author',
'au': 'author',
'name': 'author',
# exact author
'exactauthor': 'exactauthor',
'exact-author': 'exactauthor',
'ea': 'exactauthor',
# experiment
'experiment': 'experiment',
'exp': 'experiment',
'expno': 'experiment',
'sd': 'experiment',
'se': 'experiment',
# journal
'journal': 'journal',
'j': 'journal',
'published_in': 'journal',
'spicite': 'journal',
'volume': 'journal',
'vol': 'journal',
# journal page
'journalpage': 'journalpage',
'journal-page': 'journalpage',
'jp': 'journalpage',
# journal year
'journal-year': '773__y',
'jy': '773__y',
# key
'key': '970__a',
'irn': '970__a',
'record': '970__a',
'document': '970__a',
'documents': '970__a',
# keywords
'keyword': 'keyword',
'k': 'keyword',
'keywords': 'keyword',
'kw': 'keyword',
# note
'note': 'note',
# old title
'old-title': '246__a',
'old-t': '246__a',
'ex-ti': '246__a',
'et': '246__a',
# postal code
'postalcode': 'postalcode',
'zip': 'postalcode',
# ppf subject
'ppf-subject': '650__a',
'status': '650__a',
# recid
'recid': 'recid',
# bulletin
'bb': 'reportnumber',
'bbn': 'reportnumber',
'bull': 'reportnumber',
'bulletin-bd': 'reportnumber',
'bulletin-bd-no': 'reportnumber',
'eprint': 'reportnumber',
# report number
'r': 'reportnumber',
'rn': 'reportnumber',
'rept': 'reportnumber',
'report': 'reportnumber',
'report-num': 'reportnumber',
'reportnumber': 'reportnumber',
# title
'title': 'title',
't': 'title',
'ti': 'title',
'with-language': 'title',
# fulltext
'fulltext': 'fulltext',
'ft': 'fulltext',
# topic
'topic': '695__a',
'tp': '695__a',
'hep-topic': '695__a',
'desy-keyword': '695__a',
'dk': '695__a',
# doi
'doi': 'doi',
# topcite
'cited': 'cited',
'topcit': 'cited',
'topcite': 'cited',
# captions
'caption': 'caption',
# category
'arx': '037__c',
'category': '037__c',
# primarch
'parx': '037__c',
'primarch': '037__c',
# texkey
'texkey': 'texkey',
# type code
'collection': 'collection',
'tc': 'collection',
'ty': 'collection',
'type': 'collection',
'type-code': 'collection',
'scl': 'collection',
'ps': 'collection',
# field code
'subject': 'subject',
'f': 'subject',
'fc': 'subject',
'field': 'subject',
'field-code': 'subject',
# coden
'bc': 'journal',
'browse-only-indx': 'journal',
'coden': 'journal',
'journal-coden': 'journal',
# jobs specific codes
'job': 'title',
'position': 'title',
'region': 'region',
'continent': 'region',
'deadline': '046__a',
'rank': 'rank',
# cataloguer
'cataloguer': 'cataloguer',
'cat': 'cataloguer',
# hidden note
'hidden-note': '595',
'hn': '595',
# rawref
'rawref': 'rawref',
# References
'refs': 'refersto',
'refersto': 'refersto',
}


# pylint: disable=C0321,R0903


class LeafRule(ast.Leaf):

    def __init__(self):
        pass


class UnaryRule(ast.UnaryOp):

    def __init__(self):
        pass


class BinaryRule(ast.BinaryOp):

    def __init__(self):
        pass


class ListRule(ast.ListOp):

    def __init__(self):
        pass


class Whitespace(LeafRule):
    grammar = attr('value', re.compile(r"\s+"))


_ = optional(Whitespace)


class Not(object):
    grammar = omit([
        omit(re.compile(r"and\s+not", re.I)),
        re.compile(r"not", re.I),
        Literal('-'),
    ])


class And(object):
    grammar = omit([
        re.compile(r"and", re.I),
        Literal('+'),
    ])


class Or(object):
    grammar = omit([
        re.compile(r"or", re.I),
        Literal('|'),
    ])


class KeywordRule(LeafRule):
    grammar = attr('value', re.compile(r"[\w\d]+"))


class SpiresKeywordRule(LeafRule):
    grammar = attr('value', re.compile(r"(%s)\b" % "|".join(SPIRES_KEYWORDS.keys()), re.I))


class SingleQuotedString(LeafRule):
    grammar = Literal("'"), attr('value', re.compile(r"([^']|\\.)*")), Literal("'")


class DoubleQuotedString(LeafRule):
    grammar = Literal('"'), attr('value', re.compile(r'([^"]|\\.)*')), Literal('"')


class SlashQuotedString(LeafRule):
    grammar = Literal('/'), attr('value', re.compile(r"([^/]|\\.)*")), Literal('/')


class SimpleValue(LeafRule):

    def __init__(self, values):
        super(SimpleValue, self).__init__()
        self.value = "".join(v.value for v in values)


class SimpleValueUnit(LeafRule):
    grammar = [
        re.compile(r"[^\s\)\(:]+"),
        (re.compile(r'\('), SimpleValue, re.compile(r'\)')),
    ]

    def __init__(self, args):
        super(SimpleValueUnit, self).__init__()
        if isinstance(args, basestring):
            self.value = args
        else:
            self.value = args[0] + args[1].value + args[2]


SimpleValue.grammar = some(SimpleValueUnit)


class SpiresSimpleValue(LeafRule):

    def __init__(self, values):
        super(SpiresSimpleValue, self).__init__()
        self.value = "".join(v.value for v in values)


class SpiresSimpleValueUnit(LeafRule):
    grammar = [
        re.compile(r"[^\s\)\(]+"),
        (re.compile(r'\('), SpiresSimpleValue, re.compile(r'\)')),
    ]

    def __init__(self, args):
        super(SpiresSimpleValueUnit, self).__init__()
        if isinstance(args, basestring):
            self.value = args
        else:
            self.value = args[0] + args[1].value + args[2]


SpiresSimpleValue.grammar = some(SpiresSimpleValueUnit)


class SimpleRangeValue(LeafRule):
    grammar = attr('value', re.compile(r"([^\s\)\(-]|-+[^\s\)\(>])+"))


class RangeValue(UnaryRule):
    grammar = attr('op', [DoubleQuotedString, SimpleRangeValue])


class RangeOp(BinaryRule):
    grammar = (
        attr('left', RangeValue),
        Literal('->'),
        attr('right', RangeValue)
    )


class Value(UnaryRule):
    grammar = attr('op', [
        RangeOp,
        SingleQuotedString,
        DoubleQuotedString,
        SlashQuotedString,
        SimpleValue,
    ])


class Find(Keyword):
    regex = re.compile(r"(find|fin|f)", re.I)


class SpiresSmartValue(UnaryRule):

    @classmethod
    def parse(cls, parser, text, pos):  # pylint: disable=W0613
        """Match simple values excluding some Keywords like 'and' and 'or'"""
        if not text.strip():
            return text, SyntaxError("Invalid value")

        class Rule(object):
            grammar = attr('value', SpiresSimpleValue), omit(re.compile(".*"))

        try:
            tree = pypeg2.parse(text, Rule, whitespace="")
        except SyntaxError:
            return text, SyntaxError("Expected %r" % cls)
        else:
            r = tree.value

        if r.value.lower() in ('and', 'or', 'not'):
            return text, SyntaxError("Invalid value %s" % r.value)

        return text[len(r.value):], r


class SpiresValue(ast.ListOp):
    grammar = [
        (SpiresSmartValue, maybe_some(Whitespace, SpiresSmartValue)),
        Value,
    ]


class SpiresKeywordQuery(BinaryRule):
    pass


class SpiresValueQuery(UnaryRule):
    grammar = attr('op', SpiresValue)


class SpiresSimpleQuery(UnaryRule):
    grammar = attr('op', [SpiresKeywordQuery, SpiresValueQuery])


class SpiresQuery(ListRule):
    pass


class SpiresParenthesizedQuery(UnaryRule):
    grammar = (
        omit(Literal('('), _),
        attr('op', SpiresQuery),
        omit(_, Literal(')')),
    )


class SpiresNotQuery(UnaryRule):
    grammar = (
            [
                omit(re.compile(r"and\s+not", re.I)),
                omit(re.compile(r"not", re.I)),
            ],
            [
                (omit(Whitespace), attr('op', SpiresSimpleQuery)),
                (omit(_), attr('op', SpiresParenthesizedQuery)),
                (omit(Whitespace), attr('op', SpiresValueQuery)),
            ],
    )


class SpiresAndQuery(UnaryRule):
    grammar = (
        omit(re.compile(r"and", re.I)),
        [
            (omit(Whitespace), attr('op', SpiresSimpleQuery)),
            (omit(_), attr('op', SpiresParenthesizedQuery)),
                (omit(Whitespace), attr('op', SpiresValueQuery)),
        ]
    )


class SpiresOrQuery(UnaryRule):
    grammar = (
        omit(re.compile(r"or", re.I)),
        [
            (omit(Whitespace), attr('op', SpiresSimpleQuery)),
            (omit(_), attr('op', SpiresParenthesizedQuery)),
                (omit(Whitespace), attr('op', SpiresValueQuery)),
        ]
    )


SpiresQuery.grammar = attr('children', (
    [
        SpiresParenthesizedQuery,
        SpiresSimpleQuery,
    ],
    maybe_some((
        omit(_),
        [
            SpiresNotQuery,
            SpiresAndQuery,
            SpiresOrQuery,
        ]
    )),
))


class NestableKeyword(LeafRule):
    grammar = attr('value', [
        re.compile('refersto', re.I),
        re.compile('citedby', re.I),
    ])


class GreaterQuery(UnaryRule):
    grammar = (
        omit([
            Literal('>'),
            re.compile('after', re.I)
        ], _),
        attr('op', SpiresValue)
    )


class Number(LeafRule):
    grammar = attr('value', re.compile(r'\d+'))


class GreaterEqualQuery(UnaryRule):
    grammar = [
        (omit(Literal('>='), _), attr('op', SpiresValue)),
        (attr('op', Number), omit(re.compile(r'\+(?=\s|\)|$)'))),
    ]


class LowerQuery(UnaryRule):
    grammar = (
        omit([
            Literal('<'),
            re.compile('before', re.I)
        ], _),
        attr('op', SpiresValue)
    )


class LowerEqualQuery(UnaryRule):
    grammar = [
        (omit(Literal('<='), _), attr('op', SpiresValue)),
        (attr('op', Number), omit(re.compile(r'\-(?=\s|\)|$)'))),
    ]


class ValueQuery(UnaryRule):
    grammar = attr('op', Value)


SpiresKeywordQuery.grammar = [
        (
            attr('left', NestableKeyword),
            omit(_, Literal(':'), _),
            attr('right', [
                 SpiresParenthesizedQuery,
                 SpiresSimpleQuery,
                 ValueQuery
            ]),
        ),
        (
            attr('left', NestableKeyword),
            omit(Whitespace),
            attr('right', [
                 SpiresParenthesizedQuery,
                 SpiresSimpleQuery,
                 SpiresValueQuery
            ]),
        ),
        (
            attr('left', KeywordRule),
            omit(_, Literal(':'), _),
            attr('right', Value)
        ),
        (
            attr('left', SpiresKeywordRule),
            omit(Whitespace),
            attr('right', [
                GreaterEqualQuery,
                GreaterQuery,
                LowerEqualQuery,
                LowerQuery,
                SpiresValue
            ])
        ),
    ]


class Query(ListRule):
    pass


class KeywordQuery(BinaryRule):
    pass


KeywordQuery.grammar = [
    (
        attr('left', KeywordRule),
        omit(_, Literal(':'), _),
        attr('right', KeywordQuery)
    ),
    (
        attr('left', KeywordRule),
        omit(_, Literal(':'), _),
        attr('right', Value)
    ),
    (
        attr('left', KeywordRule),
        omit(_, Literal(':'), _),
        attr('right', Query)
    ),
]


class SimpleQuery(UnaryRule):
    grammar = attr('op', [KeywordQuery, ValueQuery])


class ParenthesizedQuery(UnaryRule):
    grammar = (
        omit(Literal('('), _),
        attr('op', Query),
        omit(_, Literal(')')),
    )


class NotQuery(UnaryRule):
    grammar = [
        (
            omit(Not),
            [
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('-')),
            attr('op', SimpleQuery),
        ),
    ]


class AndQuery(UnaryRule):
    grammar = [
        (
            omit(And),
            [
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('+')),
            attr('op', SimpleQuery),
        ),
    ]


class ImplicitAndQuery(UnaryRule):
    grammar = [
        attr('op', ParenthesizedQuery),
        attr('op', SimpleQuery),
    ]


class OrQuery(UnaryRule):
    grammar = [
        (
            omit(Or),
            [
                (omit(Whitespace), attr('op', SimpleQuery)),
                (omit(_), attr('op', ParenthesizedQuery)),
            ],
        ),
        (
            omit(Literal('|')),
            attr('op', SimpleQuery),
        ),
    ]


Query.grammar = attr('children', (
    [
        ParenthesizedQuery,
        SimpleQuery,
    ],
    maybe_some((
        omit(_),
        [
            NotQuery,
            AndQuery,
            OrQuery,
            ImplicitAndQuery,
        ]
    )),
))


class FindQuery(UnaryRule):
    grammar = omit(Find, Whitespace), attr('op', SpiresQuery)


class EmptyQueryRule(LeafRule):
    grammar = attr('value', re.compile(r'\s*'))


class Main(UnaryRule):
    grammar = [
        (omit(_), attr('op', [FindQuery, Query]), omit(_)),
        attr('op', EmptyQueryRule),
    ]


# pylint: enable=C0321,R0903


def load_walkers():

    class Walkers(object):
        from invenio_query_parser.ast_walkers.pypeg_to_ast_converter import PypegConverter
        from invenio_query_parser.ast_walkers.spires_to_invenio_converter import SpiresToInvenio
        from invenio_query_parser.ast_walkers.repr_printer import TreeRepr

    return Walkers


class SpiresToInvenioSyntaxConverter(object):
    def __init__(self):
        self.walkers = load_walkers()

    def parse_query(self, query):
        """Parse query string using given grammar"""
        tree = pypeg2.parse(query, Main, whitespace="")
        converter = self.walkers.PypegConverter()
        return tree.accept(converter)

    def convert_query(self, query):
        tree = self.parse_query(query)
        converter = self.walkers.PypegConverter()
        printer = self.walkers.TreeRepr()
        return tree.accept(converter).accept(printer)
