Changes
=======

Version 0.5.0 (released 2016-02-29):
------------------------------------

- Allows match unit to iterate over Sequences, i.e. tuple.
- Removes distinctions between double and single quotes.
- Adds support for allowed keywords.
- Removes nestable keywords (to be re-added in the future).
- Removes optional space after a keyword.
- `AND`, `OR` and `NOT` are only considered as keywords when
  written in caps.

Version 0.4.1 (released 2015-11-13):
------------------------------------

- Default key getter returns default value instead of raising key
  error if the key is not found inside the dictionary.

Version 0.4.0 (released 2015-11-12):
------------------------------------

- Removes support for Python 2.6.
- Adds **experimental** support for Elasticsearch query generation.
- Adds `MatchUnit` walker for testing data against a query.
- Adds Python 3.5 classifier and enables it in test matrix.
- Fixes 'not' operator usage at the beginning of the query and after
  an 'or' operator.

Version 0.3.0 (released 2015-07-29):
------------------------------------

- Allows search keywords to contain dots to point to subfield content,
  i.e. `author.name: Ellis`.

Version 0.2.0 (released 2014-12-10):
------------------------------------

- Initial public release.
- Adds Python2/Python3 compatibility layer.  (#2)
- Adds new Sphinx documentation page.  (#3)
- Adds simple inheritance for visitor pattern and separates SPIRES syntax
  parser to contrib module.  (#7)

Version 0.1.0 (release 2014-10-13):
------------------------------------

- Initial private release. Includes code developed by Alessio Deiana and
  Federico Poli.
