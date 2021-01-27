import unittest
from unittest.mock import patch
import json
import datetime
import warnings
from sqlalchemy.exc import SAWarning

from app import app, db
from models import Category
import strings
from tests.test_utils import (
    clear_database,
    create_category,
    auth_headers,
)


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        clear_database(db)

    def test_get_categories(self):
        category1 = create_category()
        category2 = create_category()

        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, [
            category1.serialize(),
            category2.serialize(),
        ])

    def test_get_categories_with_criteria(self):
        category = create_category()

        response = self.client.get('/categories?withCriteria=true')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, [category.serialize(with_criteria=True)])

    def test_get_category(self):
        category = create_category()

        response = self.client.get(f'/categories/{category.id}')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, category.serialize())

    def test_get_category_with_criteria(self):
        category = create_category()

        response = self.client.get(f'/categories/{category.id}?withCriteria=true')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, category.serialize(with_criteria=True))

    def test_get_category_doesnt_exist(self):
        response = self.client.get('/categories/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.category_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_category(self, mock_auth):
        data = {
            'title': 'Safe Work Environment',
            'help_text': 'Some help text',
        }

        response = self.client.post('/categories', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        category = Category.query.one()
        self.assertEqual(category.title, 'Safe Work Environment')
        self.assertEqual(category.help_text, 'Some help text')
        self.assertTrue(category.active)
        self.assertIsNone(category.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, category.serialize())

    def test_post_category_no_auth(self):
        response = self.client.post('/categories', data={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_category(self, mock_auth):
        category = create_category()

        data = {
            'title': 'A New Title',
            'help_text': 'Some new help text',
        }

        response = self.client.put(
            f'/categories/{category.id}',
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        category = Category.query.get(category.id)
        self.assertEqual(category.title, 'A New Title')
        self.assertEqual(category.help_text, 'Some new help text')
        self.assertTrue(category.active)
        self.assertIsNone(category.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, category.serialize())

    def test_put_category_no_auth(self):
        response = self.client.put('/categories/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_category_deactivate(self, mock_auth):
        category = create_category()

        data = {'active': False}
        response = self.client.put(
            f'/categories/{category.id}',
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        category = Category.query.first()
        self.assertFalse(category.active)
        self.assertTrue(isinstance(category.deactivated_at, datetime.datetime))

        # Category cannot be reactivated
        deactivated_at = category.deactivated_at

        data = {'active': True}
        response = self.client.put(
            f'/categories/{category.id}',
            json=data,
            headers=auth_headers(),
        )
        category = Category.query.first()
        self.assertFalse(category.active)
        self.assertEqual(category.deactivated_at, deactivated_at)
