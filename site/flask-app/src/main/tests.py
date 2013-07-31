# -*- coding: utf-8 -*-
import unittest
import main

class MainTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.app = main.app.test_client()

    def test_main(self):
        """Test rendered page."""
        rv = self.app.get('/')
        assert 'Poio Corpus' in rv.data

    def test_about(self):
        """Test rendered page."""
        rv = self.app.get('/about')
        assert 'Poio Corpus' in rv.data

    def test_get_info_for_iso(self):
        """Test query of geo information"""
        rv = main.get_info_for_iso('bar')
        assert rv == { 'label' : u'Bavarian', 'geo': { 'lat': u'47.9232', 'lon': u'13.246' } }

class RdfIsoTestCase(unittest.TestCase):

    def test_geo(self):
        """Test query of geo information"""
        rdf = main.RdfIso('bar')
        assert rdf.geo() == (u'47.9232', u'13.246')

    def test__label_for_iso(self):
        """Test query of label"""
        rdf = main.RdfIso('bar')
        assert rdf.label() == u'Bavarian'
        rdf = main.RdfIso('ast')
        assert rdf.label() == u'Asturian'

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()