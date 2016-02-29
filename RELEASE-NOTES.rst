=============================
 Invenio-Query-Parser v0.5.0
=============================

Invenio-Query-Parser v0.5.0 was released on February 29, 2016.

About
-----

Search query parser supporting Invenio and SPIRES search syntax.


Incompatible changes
--------------------

- Removes nestable keywords (to be re-added in the future).
- Removes optional space after a keyword.
- `AND`, `OR` and `NOT` are only considered as keywords when
  written in caps.

New features
------------

- Adds support for allowed keywords.

Improved features
-----------------

- Allows match unit to iterate over Sequences, i.e. tuple.
- Removes distinctions between double and single quotes.

Installation
------------

   $ pip install invenio-query-parser==0.5.0

Documentation
-------------

   http://invenio-query-parser.readthedocs.org/en/v0.5.0

Happy hacking and thanks for flying Invenio-Query-Parser.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-query-parser
|   URL: http://invenio-software.org
