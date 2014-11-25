..
    This file is part of Invenio-Query-Parser
    Copyright (C) 2014 CERN.

    Invenio-Query-Parser is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio-Query-Parser is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio-Query-Parser; if not, write to the Free Software Foundation,
    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

    In applying this licence, CERN does not waive the privileges and immunities
    granted to it by virtue of its status as an Intergovernmental Organization
    or submit itself to any jurisdiction.

======================
 Invenio-Query-Parser
======================
.. currentmodule:: invenio_query_parser

.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/invenio-query-parser">
            <img src="https://travis-ci.org/inveniosoftware/invenio-query-parser.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/invenio-query-parser">
            <img src="https://coveralls.io/repos/inveniosoftware/invenio-query-parser/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>

Search query parser supporting Invenio and SPIRES search syntax.

Contents
--------

.. contents::
   :local:
   :backlinks: none


Installation
============

Invenio-Query-Parser is on PyPI so all you need is:

.. code-block:: console

    $ pip install invenio-query-parser


Usage
=====

The easiest way is to use *pypeg2* directly with
:class:`~invenio_query_parser.parser.Main`.

.. code-block:: python

    import pypeg2
    from invenio_query_parser.parser import Main
    pypeg2.parse('author:"Ellis"', Main)


API
===

.. automodule:: invenio_query_parser
   :members:

.. automodule:: invenio_query_parser.ast
   :members:
   :undoc-members:

.. automodule:: invenio_query_parser.parser
   :members:
   :undoc-members:

.. automodule:: invenio_query_parser.visitor
   :members:
   :undoc-members:

.. include:: ../CHANGES.rst

.. include:: ../CONTRIBUTING.rst


..
    License
    =======
    .. include:: ../LICENSE

.. include:: ../AUTHORS.rst
