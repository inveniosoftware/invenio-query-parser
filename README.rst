======================
 Invenio-Query-Parser
======================

.. image:: https://github.com/inveniosoftware/invenio-query-parser/actions?query=workflow%3ACI.png?branch=master
   :target: https://github.com/inveniosoftware/invenio-query-parser/actions?query=workflow%3ACI
.. image:: https://coveralls.io/repos/inveniosoftware/invenio-query-parser/badge.png?branch=master
   :target: https://coveralls.io/r/inveniosoftware/invenio-query-parser
.. image:: https://pypip.in/v/invenio-query-parser/badge.png
   :target: https://pypi.python.org/pypi/invenio-query-parser/
.. image:: https://pypip.in/d/invenio-query-parser/badge.png
   :target: https://pypi.python.org/pypi/invenio-query-parser/
.. image:: https://readthedocs.io/projects/invenio-query-parser/badge/?version=latest
   :target: https://invenio-query-parser.readthedocs.io/


About
=====

Search query parser supporting Invenio and SPIRES search syntax.


Installation
============

Invenio-Query-Parser is on PyPI so all you need is: ::

    pip install invenio-query-parser


Documentation
=============

Documentation is readable at http://invenio-query-parser.readthedocs.io or
it can be built using Sphinx: ::

    pip install invenio-query-parser[docs]
    python setup.py build_sphinx


Testing
=======

Install the test dependencies together with one search backend
(``opensearch2``, ``opensearch1`` or ``elasticsearch7``) and run the
test suite: ::

    pip install -e ".[tests,opensearch2]"
    ./run-tests.sh
