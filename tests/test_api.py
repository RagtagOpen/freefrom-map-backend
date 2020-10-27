# https://github.com/CircleCI-Public/circleci-demo-python-flask/blob/master/tests/test_api.py
import unittest
import json
from app import app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        """Please delete this test once we have some real tests"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(json_response["message"], "Hello World!")

