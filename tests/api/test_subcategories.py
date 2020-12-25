import unittest
from unittest.mock import patch
import json
import datetime
import warnings
from sqlalchemy.exc import SAWarning

from app import app, db
from models import Subcategory
import strings
from tests.test_utils import (
    clear_database,
    create_category,
    create_subcategory,
    auth_headers,
)


class SubcategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()

    def tearDown(self):
        clear_database(db)

    def test_get_subcategories(self):
        subcategory1 = create_subcategory(self.category.id)
        subcategory2 = create_subcategory(self.category.id)

        response = self.client.get('/subcategories')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, [
            subcategory1.serialize(),
            subcategory2.serialize(),
        ])

    def test_get_subcategory_doesnt_exist(self):
        response = self.client.get('/subcategories/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.subcategory_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_subcategory(self, mock_auth):
        category_id = self.category.id
        data = {
            'category_id': category_id,
            'title': 'Safe Work Environment',
            'help_text': 'Some help text',
        }

        response = self.client.post('/subcategories', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        subcategory = Subcategory.query.one()
        self.assertEqual(subcategory.category_id, category_id)
        self.assertEqual(subcategory.title, 'Safe Work Environment')
        self.assertEqual(subcategory.help_text, 'Some help text')
        self.assertTrue(subcategory.active)
        self.assertIsNone(subcategory.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, subcategory.serialize())

    @patch('auth.is_token_valid', return_value=True)
    def test_post_subcategory_category_doesnt_exist(self, mock_auth):
        data = {'category_id': 0}
        response = self.client.post('/subcategories', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.category_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_subcategory_no_category(self, mock_auth):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/subcategories', json={}, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.category_not_found)

    def test_post_subcategory_no_auth(self):
        response = self.client.post('/subcategories', data={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_subcategory(self, mock_auth):
        category_id = self.category.id
        subcategory = create_subcategory(category_id)

        data = {
            'title': 'A New Title',
            'help_text': 'Some new help text',
        }

        response = self.client.put(
            f'/subcategories/{subcategory.id}',
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        subcategory = Subcategory.query.get(subcategory.id)
        self.assertEqual(subcategory.category_id, category_id)
        self.assertEqual(subcategory.title, 'A New Title')
        self.assertEqual(subcategory.help_text, 'Some new help text')
        self.assertTrue(subcategory.active)
        self.assertIsNone(subcategory.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, subcategory.serialize())

    @patch('auth.is_token_valid', return_value=True)
    def test_put_subcategory_cannot_change_category(self, mock_auth):
        category_id = self.category.id
        subcategory = create_subcategory(category_id)

        data = {'category_id': subcategory.category_id + 1}
        response = self.client.put(
            f'/subcategories/{subcategory.id}',
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 400)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.cannot_change_category)

    def test_put_subcategory_no_auth(self):
        response = self.client.put('/subcategories/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_subcategory_doesnt_exist(self, mock_auth):
        response = self.client.put('/subcategories/1', json={}, headers=auth_headers())
        self.assertEqual(response.status_code, 404)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.subcategory_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_subcategory_deactivate(self, mock_auth):
        subcategory = create_subcategory(self.category.id)

        data = {'active': False}
        response = self.client.put(
            f'/subcategories/{subcategory.id}',
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        subcategory = Subcategory.query.first()
        self.assertFalse(subcategory.active)
        self.assertTrue(isinstance(subcategory.deactivated_at, datetime.datetime))

        # Subcategory cannot be reactivated
        deactivated_at = subcategory.deactivated_at

        data = {'active': True}
        response = self.client.put(
            f'/subcategories/{subcategory.id}',
            json=data,
            headers=auth_headers(),
        )
        subcategory = Subcategory.query.first()
        self.assertFalse(subcategory.active)
        self.assertEqual(subcategory.deactivated_at, deactivated_at)
