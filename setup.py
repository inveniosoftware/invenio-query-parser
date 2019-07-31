#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
    'check-manifest>=0.25',
    'coverage>=4.0.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=2.1.0',
    'pytest-pep8>=1.0.6',
    'pytest-runner>=2.7.0',
    'pytest>=2.8.0',
]

setup(
    name='invenio-query-parser',
    version=version,
    url='https://github.com/inveniosoftware/invenio-query-parser',
    license='MIT',
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
    extras_require={
        'docs': [
            'sphinx_rtd_theme>=0.1.9',
        ],
        'elasticsearch': [
            'elasticsearch-dsl>=2.0.0',
        ],
        'tests': tests_require,
    },
    tests_require=tests_require,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
        ' or later (MIT+)',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
