import unittest
from unittest.mock import patch
import json
import datetime

from app import app, db
from models import Score
import strings
from tests.test_utils import clear_database, create_category, create_criterion, auth_headers


class ScoresTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()
        self.criterion = create_criterion(self.category.id)

    def tearDown(self):
        clear_database(db)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score(self, mock_auth):
        criterion_id = self.criterion.id
        data = {
            'criterion_id': criterion_id,
            'state': 'NY',
            'meets_criterion': True,
        }

        response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        score = Score.query.one()
        self.assertEqual(score.criterion_id, criterion_id)
        self.assertEqual(score.state, 'NY')
        self.assertTrue(score.meets_criterion)
        self.assertTrue(isinstance(score.created_at, datetime.datetime))

        json_response = json.loads(response.data)
        self.assertEqual(json_response, {
            'id': score.id,
            'criterion_id': criterion_id,
            'state': 'NY',
            'meets_criterion': True,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score_criterion_doesnt_exist(self, mock_auth):
        criterion_id = self.criterion.id + 1
        data = {
            'category_id': criterion_id,
        }

        response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 404)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.criterion_not_found)

    def test_post_score_no_auth(self):
        response = self.client.post('/scores', data={}, headers={})
        self.assertEqual(response.status_code, 401)
