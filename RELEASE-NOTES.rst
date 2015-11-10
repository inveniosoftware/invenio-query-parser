=============================
 Invenio-Query-Parser v0.4.0
=============================

Invenio-Query-Parser v0.4.0 was released on November 12, 2015.

About
-----

Search query parser supporting Invenio and SPIRES search syntax.

Incompatible changes
--------------------

- Removes support for Python 2.6.

New features
------------

- Adds **experimental** support for Elasticsearch query generation.
- Adds `MatchUnit` walker for testing data against a query.

Improved features
-----------------

- Adds Python 3.5 classifier and enables it in test matrix.

Bug fixes
---------

- Fixes 'not' operator usage at the beginning of the query and after
  an 'or' operator.

Installation
------------

   $ pip install invenio-query-parser==0.4.0

Documentation
-------------

   http://invenio-query-parser.readthedocs.org/en/v0.4.0

Happy hacking and thanks for flying Invenio-Query-Parser.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-query-parser
|   URL: http://invenio-software.org
