# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import unittest
import main

class MainTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.app = main.app.test_client()

    def test_main(self):
        """Test rendered index page."""
        rv = self.app.get('/')
        assert 'Poio Corpus' in rv.data

    def test_about(self):
        """Test rendered about page."""
        rv = self.app.get('/about')
        assert 'Poio Corpus' in rv.data

    def test_corpus(self):
        """Test rendered corpus page."""
        rv = self.app.get('/corpus')
        assert 'Corpus files' in rv.data

    def test_tools(self):
        """Test rendered tools page."""
        rv = self.app.get('/tools')
        assert 'Semantic maps' in rv.data
        assert 'Text prediction' in rv.data

    def test_documentation(self):
        """Test rendered documentation page."""
        rv = self.app.get('/documentation')
        assert 'readthedocs.org' in rv.data

    def test_licenses(self):
        """Test rendered licenses page."""
        rv = self.app.get('/licenses')
        assert 'Apache 2.0 License' in rv.data

    def test_privacy(self):
        """Test rendered privacy page."""
        rv = self.app.get('/privacy')
        assert 'Personal Data' in rv.data

    def test_imprint(self):
        """Test rendered imprint page."""
        rv = self.app.get('/imprint')
        assert '2395-182 Minde' in rv.data

    def test_get_semantic_map(self):
        """Test get_semantic_map."""
        rv = self.app.get('/tools/semantics/bar/brezn')
        assert 'fettn' in rv.data
        assert 'brezn' in rv.data

    def test_prediction(self):
        """Test prediction.""" 
        rv = self.app.get('/tools/prediction/bar')
        assert 'Text prediction' in rv.data

        rv = self.app.get('/_prediction?iso=bar&text=De')
        assert 'Des' in rv.data

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()