import unittest
from unittest.mock import patch
import json
import datetime

from app import app, db
from models import Category, Link
from tests.test_utils import clear_database, create_category, auth_headers


class LinksTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()

    def tearDown(self):
        clear_database(db)

    def test_get_links(self):
        link1 = Link(
            category_id=self.category.id,
            state='NY',
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        )

        link2 = Link(
            category_id=self.category.id,
            state='AZ',
            text='Statute 20 of Policy ABC',
            url='az.gov/link/to/statute',
        )

        link2.deactivate()

        Link.save_all([link1, link2])

        response = self.client.get('/links')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0], {
            'id': link1.id,
            'category_id': link1.category_id,
            'state': 'NY',
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

        link2_expected = {
            'id': link2.id,
            'category_id': link2.category_id,
            'state': 'AZ',
            'text': 'Statute 20 of Policy ABC',
            'url': 'az.gov/link/to/statute',
            'active': False,
        }

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(link2_expected.items() <= json_response[1].items())
        self.assertTrue(isinstance(json_response[1]['deactivated_at'], str))

    def test_get_links_empty(self):
        response = self.client.get('/links')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, [])

    def test_get_link(self):
        link = Link(
            category_id=self.category.id,
            state='NY',
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        ).save()

        response = self.client.get('/links/%i' % link.id)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': link.id,
            'category_id': link.category_id,
            'state': 'NY',
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    def test_get_link_doesnt_exist(self):
        response = self.client.get('/links/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response['text'], 'Link does not exist')

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link(self, mock_auth):
        data = {
            'category_id': self.category.id,
            'state': 'NY',
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
        }

        response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        new_link = Link.query.first()
        category = Category.query.first()

        self.assertEqual(new_link.category_id, category.id)
        self.assertEqual(new_link.state, 'NY')
        self.assertEqual(new_link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(new_link.url, 'ny.gov/link/to/statute')

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': new_link.id,
            'category_id': category.id,
            'state': 'NY',
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    def test_post_link_no_auth(self):
        response = self.client.post('/links', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_link(self, mock_auth):
        link = Link(state='NY', category_id=self.category.id).save()

        data = {
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
        }

        response = self.client.put('/links/%i' % link.id, json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh link object
        link = Link.query.first()
        category = Category.query.first()

        self.assertEqual(link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(link.url, 'ny.gov/link/to/statute')

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': link.id,
            'category_id': category.id,
            'state': 'NY',
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    def test_put_category_no_auth(self):
        response = self.client.put('/links/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_link_deactivate(self, mock_auth):
        link = Link(state='NY', category_id=self.category.id).save()

        data = {
            'active': False,
        }

        response = self.client.put('/links/%i' % link.id, json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh link object
        link = Link.query.first()

        self.assertFalse(link.active)
        self.assertTrue(isinstance(link.deactivated_at, datetime.datetime))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(isinstance(json_response['deactivated_at'], str))
