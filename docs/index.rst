..
    This file is part of Invenio.
    Copyright (C) 2015-2019 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


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
