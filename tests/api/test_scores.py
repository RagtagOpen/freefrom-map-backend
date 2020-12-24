import unittest
from unittest.mock import patch
import json
import datetime
import warnings
from sqlalchemy.exc import SAWarning

from app import app, db
from models import Score
import strings
from tests.test_utils import clear_database, create_state, create_category, create_criterion, auth_headers


class ScoresTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()
        self.criterion = create_criterion(self.category.id)
        self.state = create_state()

    def tearDown(self):
        clear_database(db)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score(self, mock_auth):
        criterion_id = self.criterion.id
        state = self.state.code
        data = {
            'criterion_id': criterion_id,
            'state': state,
            'meets_criterion': True,
        }

        response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        score = Score.query.one()
        self.assertEqual(score.criterion_id, criterion_id)
        self.assertEqual(score.state, state)
        self.assertTrue(score.meets_criterion)
        self.assertTrue(isinstance(score.created_at, datetime.datetime))

        json_response = json.loads(response.data)
        self.assertEqual(json_response, {
            'id': score.id,
            'criterion_id': criterion_id,
            'state': state,
            'meets_criterion': True,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score_criterion_doesnt_exist(self, mock_auth):
        criterion_id = self.criterion.id + 1
        data = {
            'criterion_id': criterion_id,
        }

        response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.criterion_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score_no_criterion(self, mock_auth):
        state = self.state.code
        data = {
            'state': state,
        }

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.criterion_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_score_no_state(self, mock_auth):
        data = {
            'criterion_id': self.criterion.id,
        }

        response = self.client.post('/scores', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.invalid_state)

    def test_post_score_no_auth(self):
        response = self.client.post('/scores', data={}, headers={})
        self.assertEqual(response.status_code, 401)
