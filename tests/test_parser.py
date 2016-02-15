# -*- coding: utf-8 -*-
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014, 2015, 2016 CERN.
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

"""Unit tests for the search engine query parsers."""

from __future__ import unicode_literals

from invenio_query_parser.ast import (
    AndOp,
    DoubleQuotedValue,
    EmptyQuery,
    GreaterEqualOp,
    GreaterOp,
    Keyword,
    KeywordOp,
    LowerEqualOp,
    LowerOp,
    NotOp,
    OrOp,
    RangeOp,
    RegexValue,
    SingleQuotedValue,
    Value,
    ValueQuery)

from invenio_query_parser.contrib.spires.ast import SpiresOp
from invenio_query_parser.utils import build_valid_keywords_grammar

from pytest import generate_tests


def generate_parser_test(query, expected):
    def func(self):
        from invenio_query_parser.walkers import repr_printer
        tree = self.parser.parse_query(query)
        printer = repr_printer.TreeRepr()
        assert tree == expected, "parsed tree: %s\nexpected tree: %s" % (
            tree.accept(printer), expected.accept(printer))
    return func


@generate_tests(generate_parser_test)  # pylint: disable=R0903
class TestParser(object):
    """Test parser functionality"""

    @classmethod
    def setup_class(cls):
        from invenio_query_parser.contrib.spires import converter
        cls.parser = converter.SpiresToInvenioSyntaxConverter()
        build_valid_keywords_grammar()

    queries = (
        ("",
         EmptyQuery('')),
        ("    \t",
         EmptyQuery('    \t')),
        ("bar",
         ValueQuery(Value('bar'))),
        ("2004",
         ValueQuery(Value('2004'))),
        ("'bar'",
         ValueQuery(SingleQuotedValue('bar'))),
        ("\"bar\"",
         ValueQuery(DoubleQuotedValue('bar'))),
        ("J. Ellis",
         AndOp(ValueQuery(Value('J.')), ValueQuery(Value('Ellis')))),
        ("$e^{+}e^{-}$",
         ValueQuery(Value('$e^{+}e^{-}$'))),

        # Basic keyword:value
        ("foo:bar",
         KeywordOp(Keyword('foo'), Value('bar'))),
        ("foo: bar",
         KeywordOp(Keyword('foo'), Value('bar'))),
        ("foo: 2004",
         KeywordOp(Keyword('foo'), Value('2004'))),
        ("999: bar",
         KeywordOp(Keyword('999'), Value('bar'))),
        ("999C5: bar",
         KeywordOp(Keyword('999C5'), Value('bar'))),
        ("999__u: bar",
         KeywordOp(Keyword('999__u'), Value('bar'))),
        ("  foo:  bar  ",
         KeywordOp(Keyword('foo'), Value('bar'))),

        # Quoted strings
        ("foo: 'bar'",
         KeywordOp(Keyword('foo'), SingleQuotedValue('bar'))),
        ("foo: \"bar\"",
         KeywordOp(Keyword('foo'), DoubleQuotedValue('bar'))),
        ("foo: /bar/",
         KeywordOp(Keyword('foo'), RegexValue('bar'))),
        ("foo: \"'bar'\"",
         KeywordOp(Keyword('foo'), DoubleQuotedValue("'bar'"))),
        ('author:"Ellis, J"',
         KeywordOp(Keyword('author'), DoubleQuotedValue("Ellis, J"))),

        # Weird values
        ("foo: \"bar",
         KeywordOp(Keyword('foo'), Value('"bar'))),
        ("foo: 'bar",
         KeywordOp(Keyword('foo'), Value("'bar"))),

        # Range queries
        ("year: 2000->2012",
         KeywordOp(Keyword('year'), RangeOp(Value('2000'), Value('2012')))),
        ("year: 2000-10->2012-09",
         KeywordOp(Keyword('year'), RangeOp(Value('2000-10'),
                                            Value('2012-09')))),
        ("cited: 3->30",
         KeywordOp(Keyword('cited'), RangeOp(Value('3'), Value('30')))),
        ('author: Albert->John',
         KeywordOp(Keyword('author'), RangeOp(Value('Albert'),
                                              Value('John')))),
        ('author: "Albert"->John',
         KeywordOp(Keyword('author'), RangeOp(DoubleQuotedValue('Albert'),
                                              Value('John')))),
        ('author: Albert->"John"',
         KeywordOp(Keyword('author'), RangeOp(Value('Albert'),
                                              DoubleQuotedValue('John')))),
        ('author: "Albert"->"John"',
         KeywordOp(Keyword('author'), RangeOp(DoubleQuotedValue('Albert'),
                                              DoubleQuotedValue('John')))),

        # Star patterns
        ("bar*",
         ValueQuery(Value('bar*'))),
        ("foo: hello*",
         KeywordOp(Keyword('foo'), Value('hello*'))),
        ("foo: 'hello*'",
         KeywordOp(Keyword('foo'), SingleQuotedValue('hello*'))),
        ("foo: \"hello*\"",
         KeywordOp(Keyword('foo'), DoubleQuotedValue('hello*'))),
        ("foo: he*o",
         KeywordOp(Keyword('foo'), Value('he*o'))),
        ("foo: he*lo*",
         KeywordOp(Keyword('foo'), Value('he*lo*'))),
        ("foo: *hello",
         KeywordOp(Keyword('foo'), Value('*hello'))),

        # Special characters in keyword:value
        ("foo: O'Shea",
         KeywordOp(Keyword('foo'), Value("O'Shea"))),
        ("foo: e(-)",
         KeywordOp(Keyword('foo'), Value('e(-)'))),
        ("foo: e(+)e(-)",
         KeywordOp(Keyword('foo'), Value('e(+)e(-)'))),
        ("title: Si-28(p(pol.),n(pol.))",
         KeywordOp(Keyword('title'), Value('Si-28(p(pol.),n(pol.))'))),

        # Unicode characters
        ("foo: пушкин",
         KeywordOp(Keyword('foo'), Value("пушкин"))),
        ("foo: Lemaître",
         KeywordOp(Keyword('foo'), Value("Lemaître"))),
        ('foo: "Lemaître"',
         KeywordOp(Keyword('foo'), DoubleQuotedValue("Lemaître"))),

        # Combined queries
        ("foo:bar foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo:bar AND foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo:bar AND foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo AND bar",
         AndOp(ValueQuery(Value('foo')), ValueQuery(Value('bar')))),
        ("foo:bar OR foo:bar",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo:bar | foo:bar",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo:bar NOT foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("foo:bar AND NOT foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("foo:bar -foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar')),
               NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("foo:bar- foo:bar",
         AndOp(KeywordOp(Keyword('foo'), Value('bar-')),
               KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar)",
         KeywordOp(Keyword('foo'), Value('bar'))),
        ("((foo:bar))",
         KeywordOp(Keyword('foo'), Value('bar'))),
        ("(((foo:bar)))",
         KeywordOp(Keyword('foo'), Value('bar'))),
        ("(foo:bar) OR foo:bar",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("foo:bar OR (foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar) OR (foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar)OR(foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar)|(foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar)| (foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("( foo:bar) OR ( foo:bar)",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo:bar) OR (foo:bar )",
         OrOp(KeywordOp(Keyword('foo'), Value('bar')),
              KeywordOp(Keyword('foo'), Value('bar')))),
        ("(foo1:bar1 OR foo2:bar2) AND (foo3:bar3 OR foo4:bar4)",
         AndOp(OrOp(KeywordOp(Keyword('foo1'), Value('bar1')),
                    KeywordOp(Keyword('foo2'), Value('bar2'))),
               OrOp(KeywordOp(Keyword('foo3'), Value('bar3')),
                    KeywordOp(Keyword('foo4'), Value('bar4'))))),
        ("foo:bar AND foo:bar AND foo:bar",
            AndOp(AndOp(KeywordOp(Keyword('foo'), Value('bar')),
                        KeywordOp(Keyword('foo'), Value('bar'))),
                  KeywordOp(Keyword('foo'), Value('bar')))),
        ("aaa +bbb -ccc +ddd",
         AndOp(AndOp(AndOp(ValueQuery(Value('aaa')),
                           ValueQuery(Value('bbb'))),
                     NotOp(ValueQuery(Value('ccc')))),
               ValueQuery(Value('ddd')))),
        ("foo:bar NOT foo:bar",
            AndOp(
                KeywordOp(Keyword('foo'), Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("foo:bar AND -foo:bar",
            AndOp(
                KeywordOp(Keyword('foo'), Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("-foo:bar",
            NotOp(KeywordOp(Keyword('foo'), Value('bar')))),
        ("-foo",
            NotOp(ValueQuery(Value('foo')))),
        ("foo:bar OR -foo:bar",
            OrOp(
                KeywordOp(Keyword('foo'), Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("foo:bar OR NOT foo:bar",
            OrOp(
                KeywordOp(Keyword('foo'), Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),
        ("bar + (NOT foo:\"Ba, r\")",
            AndOp(
                ValueQuery(Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), DoubleQuotedValue('Ba, r'))))),
        ("bar | -foo:bar",
            OrOp(
                ValueQuery(Value('bar')),
                NotOp(KeywordOp(Keyword('foo'), Value('bar'))))),

        # Spires syntax #

        # Simple query
        ("find t quark",
         SpiresOp(Keyword('t'), Value('quark'))),
        ("find a:richter",
         SpiresOp(Keyword('a'), Value('richter'))),
        ("find a:\"richter, b\"",
         SpiresOp(Keyword('a'), DoubleQuotedValue('richter, b'))),

        # Simple query with non-obvious values
        ("find a richter, b",
         SpiresOp(Keyword('a'), Value('richter, b'))),
        ("find texkey Allison:1980vw",
         SpiresOp(Keyword('texkey'), Value('Allison:1980vw'))),
        ("find title bbb:ccc ddd:eee",
         SpiresOp(Keyword('title'), Value('bbb:ccc ddd:eee'))),
        ("find da today-2",
         SpiresOp(Keyword('da'), Value('today-2'))),
        ("find da today - 2",
         SpiresOp(Keyword('da'), Value('today - 2'))),
        ("find da 2012-01-01",
         SpiresOp(Keyword('da'), Value('2012-01-01'))),
        ("find t quark andorinword",
         SpiresOp(Keyword('t'), Value('quark andorinword'))),

        # Simple query with spaces
        ("find t quark   ",
         SpiresOp(Keyword('t'), Value('quark'))),
        ("   find t quark   ",
         SpiresOp(Keyword('t'), Value('quark'))),
        ("find t quark ellis  ",
         SpiresOp(Keyword('t'), Value('quark ellis'))),

        # Combined queries
        ("find t quark AND a ellis",
         AndOp(SpiresOp(Keyword('t'), Value('quark')),
               SpiresOp(Keyword('a'), Value('ellis')))),
        ("find t quark OR a ellis",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find (t aaa OR t bbb OR t ccc)OR t ddd",
         OrOp(OrOp(OrOp(SpiresOp(Keyword('t'), Value('aaa')),
                        SpiresOp(Keyword('t'), Value('bbb'))),
                   SpiresOp(Keyword('t'), Value('ccc'))),
              SpiresOp(Keyword('t'), Value('ddd')))),
        ("find a:richter AND t quark",
         AndOp(SpiresOp(Keyword('a'), Value('richter')),
               SpiresOp(Keyword('t'), Value('quark')))),
        ("find (t quark) OR (a ellis)",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find (t quark OR a ellis)",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find ((t quark) OR (a ellis))",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find (( t quark )OR( a ellis ))",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find (( t quark )OR( a:ellis ))",
         OrOp(SpiresOp(Keyword('t'), Value('quark')),
              SpiresOp(Keyword('a'), Value('ellis')))),
        ("find collaboration LIGO AND a whiting, b f AND a Weiss, r",
         AndOp(
             AndOp(
                 SpiresOp(Keyword('collaboration'), Value('LIGO')),
                 SpiresOp(Keyword('a'), Value('whiting, b f'))),
             SpiresOp(Keyword('a'), Value('Weiss, r')))),
        ("find (collaboration LIGO AND a whiting, b f) AND a Weiss, r",
         AndOp(
             AndOp(
                 SpiresOp(Keyword('collaboration'), Value('LIGO')),
                 SpiresOp(Keyword('a'), Value('whiting, b f'))),
             SpiresOp(Keyword('a'), Value('Weiss, r')))),
        ("find collaboration LIGO AND (a whiting, b f AND a Weiss, r)",
         AndOp(
             SpiresOp(Keyword('collaboration'), Value('LIGO')),
             AndOp(
                 SpiresOp(Keyword('a'), Value('whiting, b f')),
                 SpiresOp(Keyword('a'), Value('Weiss, r'))))),
        ("find (aff IMPERIAL AND d <1989 AND a ELLISON) OR"
         "(a ELLISON AND aff RIVERSIDE AND tc P)",
         OrOp(
             AndOp(
                 AndOp(
                     SpiresOp(Keyword('aff'), Value('IMPERIAL')),
                     SpiresOp(Keyword('d'), LowerOp(Value('1989')))),
                 SpiresOp(Keyword('a'), Value('ELLISON'))),
             AndOp(
                 AndOp(
                     SpiresOp(Keyword('a'), Value('ELLISON')),
                     SpiresOp(Keyword('aff'), Value('RIVERSIDE'))),
                 SpiresOp(Keyword('tc'), Value('P'))))
         ),
        ("find (a ELLISON AND aff RIVERSIDE AND tc P) OR"
         "(aff IMPERIAL AND d <1989 AND a ELLISON)",
         OrOp(
             AndOp(
                 AndOp(
                     SpiresOp(Keyword('a'), Value('ELLISON')),
                     SpiresOp(Keyword('aff'), Value('RIVERSIDE'))),
                 SpiresOp(Keyword('tc'), Value('P'))),
             AndOp(
                 AndOp(
                     SpiresOp(Keyword('aff'), Value('IMPERIAL')),
                     SpiresOp(Keyword('d'), LowerOp(Value('1989')))),
                 SpiresOp(Keyword('a'), Value('ELLISON'))))
         ),

        # Implicit keyword
        ("find a john AND ellis",
         AndOp(SpiresOp(Keyword('a'), Value('john')),
               SpiresOp(Keyword('a'), Value('ellis')))),
        ("find a john AND (ellis OR albert)",
         AndOp(SpiresOp(Keyword('a'), Value('john')),
               OrOp(ValueQuery(Value('ellis')),
                    ValueQuery(Value('albert'))))),
        ("find a john AND t quark OR higgs",
         OrOp(AndOp(SpiresOp(Keyword('a'), Value('john')),
                    SpiresOp(Keyword('t'), Value('quark'))),
              SpiresOp(Keyword('t'), Value('higgs')))),
        ("find john AND t quark OR higgs",
         OrOp(AndOp(ValueQuery(Value('john')),
                    SpiresOp(Keyword('t'), Value('quark'))),
              SpiresOp(Keyword('t'), Value('higgs')))),
        ("find a l everett OR t light higgs AND j phys.rev.lett. AND "
         "primarch hep-ph",
         AndOp(AndOp(OrOp(SpiresOp(Keyword('a'), Value('l everett')),
                          SpiresOp(Keyword('t'), Value('light higgs'))),
                     SpiresOp(Keyword('j'), Value('phys.rev.lett.'))),
               SpiresOp(Keyword('primarch'), Value('hep-ph')))),
        ("find a l everett OR t light higgs AND j phys.rev.lett. AND monkey",
         AndOp(AndOp(OrOp(SpiresOp(Keyword('a'), Value('l everett')),
                          SpiresOp(Keyword('t'), Value('light higgs'))),
                     SpiresOp(Keyword('j'), Value('phys.rev.lett.'))),
               SpiresOp(Keyword('j'), Value('monkey')))),

        # Greater, Lower Ops
        ("find date > 1984",
         SpiresOp(Keyword('date'), GreaterOp(Value('1984')))),
        ("find ac > 5",
         SpiresOp(Keyword('ac'), GreaterOp(Value('5')))),
        ("find date after 1984",
         SpiresOp(Keyword('date'), GreaterOp(Value('1984')))),
        ("find date < 1984",
         SpiresOp(Keyword('date'), LowerOp(Value('1984')))),
        ("find ac < 5",
         SpiresOp(Keyword('ac'), LowerOp(Value('5')))),
        ("find date before 1984",
         SpiresOp(Keyword('date'), LowerOp(Value('1984')))),
        ("find date >= 1984",
         SpiresOp(Keyword('date'), GreaterEqualOp(Value('1984')))),
        ("find date <= 2014-10-01",
         SpiresOp(Keyword('date'), LowerEqualOp(Value('2014-10-01')))),
        ("find du > today-2",
         SpiresOp(Keyword('du'), GreaterOp(Value('today-2')))),
        ("find du > today - 2",
         SpiresOp(Keyword('du'), GreaterOp(Value('today - 2')))),
        ("find topcite 200+",
         SpiresOp(Keyword('topcite'), GreaterEqualOp(Value('200')))),
        ("find topcite 200-",
         SpiresOp(Keyword('topcite'), LowerEqualOp(Value('200')))),

        # Journal searches with whitespaces
        ("find j Phys.Rev.,D41,2330",
         SpiresOp(Keyword('j'), Value('Phys.Rev.,D41,2330'))),
        ("find j Phys.Rev.,D41, 2330",
         SpiresOp(Keyword('j'), Value('Phys.Rev.,D41, 2330'))),

        # Popular queries
        ("arXiv:1004.0648",
         KeywordOp(Keyword('arXiv'), Value("1004.0648"))),
        ("find ea chowdhury, borun d",
         SpiresOp(Keyword('ea'), Value("chowdhury, borun d"))),
        ("(author:'Hiroshi Okada' OR (author:'H Okada' hep-ph) OR "
         "title: 'Dark matter in supersymmetric U(1(B-L) model' OR "
         "title: 'Non-Abelian discrete symmetry for flavors')",
         OrOp(OrOp(OrOp(KeywordOp(Keyword('author'),
                                  SingleQuotedValue('Hiroshi Okada')),
                        AndOp(KeywordOp(Keyword('author'),
                                        SingleQuotedValue('H Okada')),
                              ValueQuery(Value('hep-ph')))),
                   KeywordOp(Keyword('title'),
                             SingleQuotedValue('Dark matter in supersymmetric '
                                               'U(1(B-L) model'))),
              KeywordOp(Keyword('title'), SingleQuotedValue(
                  'Non-Abelian discrete symmetry for flavors')))),
        ("f a Oleg Antipin",
         SpiresOp(Keyword('a'), Value('Oleg Antipin'))),
        ("FIND a Oleg Antipin",
         SpiresOp(Keyword('a'), Value('Oleg Antipin'))),
        ("f a rodrigo,g AND NOT rodrigo,j",
         AndOp(SpiresOp(Keyword('a'), Value('rodrigo,g')),
               NotOp(SpiresOp(Keyword('a'), Value('rodrigo,j'))))),

        # Dotable keys
        ("foo.bar:baz",
         KeywordOp(Keyword('foo.bar'), Value('baz'))),
        ("a.b.c.d.f:bar",
         KeywordOp(Keyword('a.b.c.d.f'), Value('bar'))),
    )


def test_parser_with_context(app):
    """Test parser with application context."""
    queries = (
        ("",
         EmptyQuery('')),
        ("    \t",
         EmptyQuery('    \t')),
        ("bar",
         ValueQuery(Value('bar'))),
        ("2004",
         ValueQuery(Value('2004'))),
        ("'bar'",
         ValueQuery(SingleQuotedValue('bar'))),
        ("\"bar\"",
         ValueQuery(DoubleQuotedValue('bar'))),
        ("J. Ellis",
         AndOp(ValueQuery(Value('J.')), ValueQuery(Value('Ellis')))),
        ("$e^{+}e^{-}$",
         ValueQuery(Value('$e^{+}e^{-}$'))),
        ("foo:somthing",
         AndOp(ValueQuery(Value('foo:')), ValueQuery(Value('somthing')))),
        ("foo:bar:somthing",
         AndOp(ValueQuery(Value('foo:bar:')), ValueQuery(Value('somthing')))),
        ("title:bar:somthing",
         KeywordOp(Keyword('title'), Value('bar:somthing'))),
        ("035__a:oai:arXiv.org:1503.06238",
         KeywordOp(Keyword('035__a'), Value('oai:arXiv.org:1503.06238'))),
    )

    with app.app_context():
        from invenio_query_parser.walkers import repr_printer
        from invenio_query_parser.contrib.spires import converter
        build_valid_keywords_grammar()
        parser = converter.SpiresToInvenioSyntaxConverter()

        for count, args in enumerate(queries):
            tree = parser.parse_query(args[0])
            printer = repr_printer.TreeRepr()
            assert tree == args[1], "parsed tree: %s\nexpected tree: %s" % (
                tree.accept(printer), args[1].accept(printer))
