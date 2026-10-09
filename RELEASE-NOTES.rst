=============================
 Invenio-Query-Parser v0.7.0
=============================

Invenio-Query-Parser v0.7.0 was released on October 9th, 2026.

About
-----

Search query parser supporting Invenio and SPIRES search syntax.

Incompatible changes
--------------------

- Drops support for Python versions older than 3.9.
- Search DSL walker now uses ``invenio_search.api.dsl`` instead of
  ``elasticsearch_dsl`` directly; the ``elasticsearch`` extra is replaced
  by ``elasticsearch7``, ``opensearch1`` and ``opensearch2`` extras.

Bug fixes
---------

- Fixes imports for Python upgrade.
- Fixes errors surfaced by the updated test suite and CI image.

Installation
------------

   $ pip install invenio-query-parser==0.7.0

Documentation
-------------

   http://invenio-query-parser.readthedocs.io/en/v0.7.0

Happy hacking and thanks for flying Invenio-Query-Parser.

| Invenio Development Team
|   Email: info@inveniosoftware.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: https://github.com/inveniosoftware/invenio-query-parser
|   URL: http://inveniosoftware.org
