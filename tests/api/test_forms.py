import unittest
from unittest.mock import patch
import json

from app import app, db
import strings
from tests.test_utils import clear_database


class FormsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        clear_database(db)

    @patch('app.services.post_google')
    def test_submit_form(self, mock_post):
        data = {
            'useful': True,
            'useful_desc': 'I learned a lot!',
            'learned': True,
            'usage_plan': '',
            'suggestions': '',
        }
        # we add a 'form' field to the payload sent to the Google API
        google_payload = data.copy()
        google_payload['form'] = 'give-feedback'
        mock_post.return_value = google_payload

        response = self.client.post('/forms/give-feedback', json=data)
        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once_with(google_payload)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, mock_post.return_value)

    @patch('app.services.post_google')
    def test_submit_form_doesnt_exist(self, mock_post):
        response = self.client.post('/forms/random_form', json={})
        self.assertEqual(response.status_code, 400)
        mock_post.assert_not_called()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.form_not_found)

    @patch('app.services.post_google', return_value={'result': 'error'})
    def test_submit_form_google_error(self, mock_post):
        response = self.client.post('/forms/feedback', json={})
        self.assertEqual(response.status_code, 500)
        mock_post.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.internal_server_error)
