import os
import unittest
from app import create_app


class CapstoneTestCase(unittest.TestCase):
    """This class represents the app test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_index(self):
        """Test get_index """
        res = self.client().get("/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["msg"], "Hello")
