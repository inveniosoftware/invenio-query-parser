# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration of SPIRES parser."""

SPIRES_KEYWORDS = {
    # address
    'address': 'address',
    # affiliation
    'affiliation': 'affiliation',
    'affil': 'affiliation',
    'aff': 'affiliation',
    'af': 'affiliation',
    'institution': 'affiliation',
    'inst': 'affiliation',
    # any field
    'anyfield': 'anyfield',
    'any': 'anyfield',
    # author count
    'authorcount': 'authorcount',
    'ac': 'authorcount',
    # citation / reference
    'reference': 'reference',
    'c': 'refersto',
    'citation': 'reference',
    'citedby': 'citedby',
    'jour-vol-page': 'reference',
    'jvp': 'reference',
    # collaboration
    'collaboration': 'collaboration',
    'collab-name': 'collaboration',
    'cn': 'collaboration',
    # conference number
    'confnumber': 'confnumber',
    'conf-number': 'confnumber',
    'cnum': 'confnumber',
    # country
    'country': 'country',
    'cc': 'country',
    # date
    'date': 'year',
    'd': 'year',
    # date added
    'date-added': 'datecreated',
    'dadd': 'datecreated',
    'da': 'datecreated',
    # date updated
    'date-updated': 'datemodified',
    'dupd': 'datemodified',
    'du': 'datemodified',
    # first author
    'firstauthor': 'firstauthor',
    'first-author': 'firstauthor',
    'fa': 'firstauthor',
    # author
    'author': 'author',
    'a': 'author',
    'au': 'author',
    'name': 'author',
    # exact author
    'exactauthor': 'exactauthor',
    'exact-author': 'exactauthor',
    'ea': 'exactauthor',
    # experiment
    'experiment': 'experiment',
    'exp': 'experiment',
    'expno': 'experiment',
    'sd': 'experiment',
    'se': 'experiment',
    # journal
    'journal': 'journal',
    'j': 'journal',
    'published_in': 'journal',
    'spicite': 'journal',
    'volume': 'journal',
    'vol': 'journal',
    # journal page
    'journalpage': 'journalpage',
    'journal-page': 'journalpage',
    'jp': 'journalpage',
    # journal year
    'journal-year': '773__y',
    'jy': '773__y',
    # key
    'key': '970__a',
    'irn': '970__a',
    'record': '970__a',
    'document': '970__a',
    'documents': '970__a',
    # keywords
    'keyword': 'keyword',
    'k': 'keyword',
    'keywords': 'keyword',
    'kw': 'keyword',
    # note
    'note': 'note',
    # old title
    'old-title': '246__a',
    'old-t': '246__a',
    'ex-ti': '246__a',
    'et': '246__a',
    # postal code
    'postalcode': 'postalcode',
    'zip': 'postalcode',
    # ppf subject
    'ppf-subject': '650__a',
    'status': '650__a',
    # recid
    'recid': 'recid',
    # bulletin
    'bb': 'reportnumber',
    'bbn': 'reportnumber',
    'bull': 'reportnumber',
    'bulletin-bd': 'reportnumber',
    'bulletin-bd-no': 'reportnumber',
    'eprint': 'reportnumber',
    # report number
    'r': 'reportnumber',
    'rn': 'reportnumber',
    'rept': 'reportnumber',
    'report': 'reportnumber',
    'report-num': 'reportnumber',
    'reportnumber': 'reportnumber',
    # title
    'title': 'title',
    't': 'title',
    'ti': 'title',
    'with-language': 'title',
    # fulltext
    'fulltext': 'fulltext',
    'ft': 'fulltext',
    # topic
    'topic': '695__a',
    'tp': '695__a',
    'hep-topic': '695__a',
    'desy-keyword': '695__a',
    'dk': '695__a',
    # doi
    'doi': 'doi',
    # topcite
    'cited': 'cited',
    'topcit': 'cited',
    'topcite': 'cited',
    # captions
    'caption': 'caption',
    # category
    'arx': '037__c',
    'category': '037__c',
    # primarch
    'parx': '037__c',
    'primarch': '037__c',
    # texkey
    'texkey': 'texkey',
    # type code
    'collection': 'collection',
    'tc': 'collection',
    'ty': 'collection',
    'type': 'collection',
    'type-code': 'collection',
    'scl': 'collection',
    'ps': 'collection',
    # field code
    'subject': 'subject',
    'f': 'subject',
    'fc': 'subject',
    'field': 'subject',
    'field-code': 'subject',
    # coden
    'bc': 'journal',
    'browse-only-indx': 'journal',
    'coden': 'journal',
    'journal-coden': 'journal',
    # jobs specific codes
    'job': 'title',
    'position': 'title',
    'region': 'region',
    'continent': 'region',
    'deadline': '046__a',
    'rank': 'rank',
    # cataloguer
    'cataloguer': 'cataloguer',
    'cat': 'cataloguer',
    # hidden note
    'hidden-note': '595',
    'hn': '595',
    # rawref
    'rawref': 'rawref',
    # References
    'refs': 'refersto',
    'refersto': 'refersto',
}
