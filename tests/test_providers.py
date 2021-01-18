import unittest
from unittest.mock import Mock, patch
import json
import os

from providers import post_google


class ProvidersTestCase(unittest.TestCase):
    @patch('requests.post')
    def test_post_google(self, mock_post):
        google_id = os.environ.get('GOOGLE_DEPLOYMENT_ID')
        url = f'https://script.google.com/macros/s/{google_id}/exec'
        headers = {'Content-Type': 'application/json'}

        data = {
            'form': 'feedback',
            'useful': True,
            'useful_desc': 'I learned a lot!',
            'learned': True,
            'usage_plan': '',
            'suggestions': '',
        }
        mock_post.return_value = Mock(
            status_code=201,
            text=json.dumps(data),
        )

        response = post_google(data)
        mock_post.assert_called_once_with(url, json=data, headers=headers)

        self.assertEqual(response, json.loads(mock_post.return_value.text))
