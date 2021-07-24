import unittest
from unittest.mock import patch
import json
import datetime
import warnings
from sqlalchemy.exc import SAWarning

from app import app, db
from models import Category, ResourceLink
import strings
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    auth_headers,
)


class ResourceLinksTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()
        self.state1_code = 'NY'
        self.state2_code = 'AZ'
        create_state(code=self.state1_code)
        create_state(code=self.state2_code)

    def tearDown(self):
        clear_database(db)

    def test_get_links(self):
        link1 = ResourceLink(
            category_id=self.category.id,
            state=self.state1_code,
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        )

        link2 = ResourceLink(
            category_id=self.category.id,
            state=self.state2_code,
            text='Statute 20 of Policy ABC',
            url='az.gov/link/to/statute',
        )

        link2.deactivate()

        ResourceLink.save_all([link1, link2])

        response = self.client.get('/links')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0], {
            'id': link1.id,
            'category_id': link1.category_id,
            'state': self.state1_code,
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
        link = ResourceLink(
            category_id=self.category.id,
            state=self.state1_code,
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        ).save()

        response = self.client.get('/links/%i' % link.id)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': link.id,
            'category_id': link.category_id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    def test_get_link_doesnt_exist(self):
        response = self.client.get('/links/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.link_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link(self, mock_auth):
        data = {
            'category_id': self.category.id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'type': strings.resource_link,
        }

        response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        new_link = ResourceLink.query.first()
        category = Category.query.first()

        self.assertEqual(new_link.category_id, category.id)
        self.assertEqual(new_link.state, self.state1_code)
        self.assertEqual(new_link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(new_link.url, 'ny.gov/link/to/statute')

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': new_link.id,
            'category_id': category.id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link_no_type(self, mock_auth):
        data = {
            'category_id': self.category.id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
        }

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.require_link_type)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link_invalid_type(self, mock_auth):
        data = {
            'category_id': self.category.id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'type': '',
        }

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.invalid_link_type)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link_no_category(self, mock_auth):
        data = {
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'type': strings.resource_link,
            'url': 'ny.gov/link/to/statute',
        }

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.category_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_link_no_state(self, mock_auth):
        data = {
            'category_id': self.category.id,
            'text': 'Section 20 of Statute 39-B',
            'type': strings.resource_link,
            'url': 'ny.gov/link/to/statute',
        }

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=SAWarning)
            response = self.client.post('/links', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.invalid_state)

    def test_post_link_no_auth(self):
        response = self.client.post('/links', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_link(self, mock_auth):
        link = ResourceLink(state=self.state1_code, category_id=self.category.id).save()

        data = {
            'text': 'Section 20 of Statute 39-B',
            'type': strings.resource_link,
            'url': 'ny.gov/link/to/statute',
        }

        response = self.client.put('/links/%i' % link.id, json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh link object
        link = ResourceLink.query.first()
        category = Category.query.first()

        self.assertEqual(link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(link.url, 'ny.gov/link/to/statute')

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': link.id,
            'category_id': category.id,
            'state': self.state1_code,
            'text': 'Section 20 of Statute 39-B',
            'url': 'ny.gov/link/to/statute',
            'active': True,
            'deactivated_at': None,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_put_link_cannot_change_state(self, mock_auth):
        link = ResourceLink(state=self.state1_code, category_id=self.category.id).save()

        data = {
            'state': self.state2_code,
        }

        response = self.client.put('/links/%i' % link.id, json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 400)

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.cannot_change_state)

    def test_put_category_no_auth(self):
        response = self.client.put('/links/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_link_deactivate(self, mock_auth):
        link = ResourceLink(state=self.state1_code, category_id=self.category.id).save()

        data = {
            'active': False,
        }

        response = self.client.put('/links/%i' % link.id, json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        # Refresh link object
        link = ResourceLink.query.first()

        self.assertFalse(link.active)
        self.assertTrue(isinstance(link.deactivated_at, datetime.datetime))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(isinstance(json_response['deactivated_at'], str))
