# -*- coding: utf-8 -*-
import unittest
import main
import __init__

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
        graphdata = __init__.get_semantic_map("bar", "brezn")
        assert len(graphdata) == 50
        assert graphdata[0][0] == u'brezn'

        rv = self.app.get('/tools/semantics/bar/brezn')
        assert 'brezn' in rv.data
        assert 'effentlichkeit' in rv.data

    def test_prediction(self):
        """Test prediction.""" 
        rv = self.app.get('/tools/prediction/bar?text=brez')
        assert 'Text prediction' in rv.data
        #assert 'Brezn' in rv.data


    # def test_get_info_for_iso(self):
    #     """Test query of geo information"""
    #     rv = main.get_info_for_iso('bar')
    #     assert rv == { 'label' : u'Bavarian', 'geo': { 'lat': u'47.9232', 'lon': u'13.246' } }

# class RdfIsoTestCase(unittest.TestCase):

#     def test_geo(self):
#         """Test query of geo information"""
#         rdf = main.RdfIso('bar')
#         assert rdf.geo() == (u'47.9232', u'13.246')

#     def test__label_for_iso(self):
#         """Test query of label"""
#         rdf = main.RdfIso('bar')
#         assert rdf.label() == u'Bavarian'
#         rdf = main.RdfIso('ast')
#         assert rdf.label() == u'Asturian'

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()