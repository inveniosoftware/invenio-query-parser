#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name="invenio-query-parser",
      version='0.1',
      description="Parses invenio and spires syntax.",
      author="Alessio Deiana",
      author_email="adeiana@gmail.com",
      url="git@github.com:osso/invenio-query-parser.git",
      packages=find_packages(),
      include_package_data=True,
      setup_requires=['setuptools-git'],
      install_requires=['pypeg2', 'ordereddict'],
      )
