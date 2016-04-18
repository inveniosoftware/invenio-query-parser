=============================
 Invenio-Query-Parser v0.6.0
=============================

Invenio-Query-Parser v0.6.0 was released on April 18, 2016.

About
-----

Search query parser supporting Invenio and SPIRES search syntax.

Incompatible changes
--------------------

- Removes check for Flask application context from
  `build_valid_keywords_grammar` function in favor of new `keywords`
  argument.
- Elastic search DSL walker returns instance of `elasticsearch_dsl.Q`
  instead of `dict`.

Installation
------------

   $ pip install invenio-query-parser==0.6.0

Documentation
-------------

   http://invenio-query-parser.readthedocs.org/en/v0.6.0

Happy hacking and thanks for flying Invenio-Query-Parser.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-query-parser
|   URL: http://invenio-software.org
