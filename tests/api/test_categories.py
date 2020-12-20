import unittest
from unittest.mock import patch
import json
import datetime

from app import app, db
from models import Category
from tests.test_utils import clear_database, create_category, create_criterion, auth_headers


class CategoriesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        clear_database(db)

    def test_get_categories(self):
        category1 = Category(
            title='Definition of Domestic Violence',
            help_text="This is how a state legally defines the term 'domestic violence'",
        )
        category2 = Category(
            title='Worker Protections',
            help_text=(
                'This category defines whether the state protects the jobs of victims of '
                'domestic violence'
            ),
        )
        category2.deactivate()
        Category.save_all([category1, category2])

        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(json_response), 2)

        self.assertEqual(json_response[0], {
            'id': category1.id,
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
            'active': True,
            'deactivated_at': None,
        })

        category_2_expected = {
            'id': category2.id,
            'title': 'Worker Protections',
            'help_text':
                'This category defines whether the state protects the jobs of victims of '
                'domestic violence',
            'active': False,
        }

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(category_2_expected.items() <= json_response[1].items())

    def test_get_categories_with_criteria(self):
        category = create_category()
        criterion = create_criterion(category.id)

        response = self.client.get('/categories?withCriteria=true')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data)
        self.assertEqual(len(json_response), 1)

        self.assertEqual(json_response[0], {
            'id': category.id,
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
            'active': True,
            'deactivated_at': None,
            'criteria': [criterion.serialize()],
        })

    def test_get_categories_empty(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, [])

    def test_get_category(self):
        category = Category(
            title='Definition of Domestic Violence',
            help_text="This is how a state legally defines the term 'domestic violence'",
        ).save()

        response = self.client.get('/categories/%i' % category.id)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': category.id,
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
            'active': True,
            'deactivated_at': None,
        })

    def test_get_category_with_criteria(self):
        category = Category(
            title='Definition of Domestic Violence',
            help_text="This is how a state legally defines the term 'domestic violence'",
        ).save()
        criterion = create_criterion(category.id)

        response = self.client.get('/categories/%i?withCriteria=true' % category.id)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': category.id,
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
            'active': True,
            'deactivated_at': None,
            'criteria': [criterion.serialize()],
        })

    def test_get_category_doesnt_exist(self):
        response = self.client.get('/categories/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response['text'], 'Category does not exist')

    @patch('auth.is_token_valid', return_value=True)
    def test_post_category(self, mock_auth):
        data = {
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
        }

        response = self.client.post('/categories', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        new_category = Category.query.first()
        self.assertEqual(new_category.title, 'Definition of Domestic Violence')
        self.assertEqual(
            new_category.help_text,
            "This is how a state legally defines the term 'domestic violence'",
        )

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': new_category.id,
            'title': 'Definition of Domestic Violence',
            'help_text': "This is how a state legally defines the term 'domestic violence'",
            'active': True,
            'deactivated_at': None,
        })

    def test_post_category_no_auth(self):
        response = self.client.post('/categories', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_category(self, mock_auth):
        category = create_category()

        data = {
            'title': 'A New Title',
            'help_text': 'Some new help text',
        }

        response = self.client.put(
            '/categories/%i' % category.id,
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh category object
        category = Category.query.first()

        self.assertEqual(category.title, 'A New Title')
        self.assertEqual(category.help_text, 'Some new help text')

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': category.id,
            'title': 'A New Title',
            'help_text': 'Some new help text',
            'active': True,
            'deactivated_at': None,
        })

    def test_put_category_no_auth(self):
        response = self.client.put('/categories/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_category_deactivate(self, mock_auth):
        category = create_category()

        data = {
            'active': False,
        }

        response = self.client.put(
            '/categories/%i' % category.id,
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh category object
        category = Category.query.first()

        self.assertFalse(category.active)
        self.assertTrue(isinstance(category.deactivated_at, datetime.datetime))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(isinstance(json_response['deactivated_at'], str))

        # Category cannot be reactivated
        deactivated_at = category.deactivated_at
        data = {
            'active': True,
        }

        response = self.client.put(
            '/categories/%i' % category.id,
            json=data,
            headers=auth_headers(),
        )
        category = Category.query.first()
        self.assertFalse(category.active)
        self.assertEqual(category.deactivated_at, deactivated_at)
