# -*- coding: utf-8 -*-
import unittest
import main

class MainTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.app = main.app.test_client()
        #hello.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        pass

    def test_main(self):
        """Test rendered page."""
        rv = self.app.get('/')
        assert 'Hello World!' in rv.data


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()