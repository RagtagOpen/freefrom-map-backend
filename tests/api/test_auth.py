import unittest
import json
import requests
import os

from app import app, db
from tests.test_utils import auth_headers, require_auth0_secrets

class TestAuth(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def test_private_endpoint_no_auth(self):
    response = self.client.get("/api/private")
    self.assertEqual(response.status_code, 401)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["description"], "Authorization header is expected")

  @require_auth0_secrets()
  def test_private_endpoint_auth(self):
    response = self.client.get("/api/private", headers=auth_headers())
    self.assertEqual(response.status_code, 200)
