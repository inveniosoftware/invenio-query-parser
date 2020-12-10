#!/usr/bin/env python
#
# This file is part of Invenio-Query-Parser.
# Copyright (C) 2014, 2016 CERN.
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

"""Search query parser supporting Invenio and SPIRES search syntax."""

import os
import re
import sys

from setuptools import find_packages, setup


# Get the version string.  Cannot be done with import!
with open(os.path.join('invenio_query_parser', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

tests_require = [
    'pytest-cache>=1.0',
    'pytest-runner>=2.7.0',
    'pytest-invenio>=1.4.0'
]

extras_require = {
    'docs': [
        'sphinx_rtd_theme>=0.1.9',
    ],
    'elasticsearch': [
        'elasticsearch-dsl>=2.0.0',
    ],
    'tests': tests_require,
}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup(
    name='invenio-query-parser',
    version=version,
    url='https://github.com/inveniosoftware/invenio-query-parser',
    license='GPLv2',
    author='Invenio collaboration',
    author_email='info@inveniosoftware.org',
    description='Search query parser supporting Invenio and SPIRES '
        'search syntax.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    install_requires=[
        'pypeg2>=2.15.2',
        'ordereddict>=1.1',
        'six>=1.10.0',
    ],
    extras_require=extras_require,
    tests_require=tests_require,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2'
        ' or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
