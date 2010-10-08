# -*- coding: utf-8 -*-

import doctest, os, glob

CUR_DIR = os.path.dirname(__file__)

# doctest files
doctest_files = [os.path.split(f)[1] for f in glob.glob('%s/*.txt' % here)]
doctest_files.sort()

def suite():
    suites = []
    for f in doctest_files:
        try:
            suites.append(doctest.DocFileSuite(f, encoding='utf-8'))
        except TypeError:
            suites.append(doctest.DocFileSuite(f))

