import unittest
from unittest.mock import patch
import json
import datetime

from app import app, db
from models import Criterion
import strings
from tests.test_utils import clear_database, create_category, create_criterion, auth_headers


class CriteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()

    def tearDown(self):
        clear_database(db)

    def test_get_criteria(self):
        criterion1 = Criterion(
            category_id=self.category.id,
            title='Includes economic abuse framework',
            recommendation_text=(
                "The state's definition of domestic violence should include a framework of "
                'economic abuse'
            ),
            help_text=(
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence'
            ),
            adverse=False,
        )

        criterion2 = Criterion(
            category_id=self.category.id,
            title='Uses coercive control framework',
            recommendation_text=(
                "The state's definition of domestic violence should use a framework of coercive "
                'control'
            ),
            help_text=(
                'This means that the state acknowledges the role that coercion can play in '
                'domestic violence'
            ),
            adverse=True,
        )

        criterion2.deactivate()
        Criterion.save_all([criterion1, criterion2])

        response = self.client.get('/criteria')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0], {
            'id': criterion1.id,
            'category_id': criterion1.category_id,
            'title': 'Includes economic abuse framework',
            'recommendation_text':
                "The state's definition of domestic violence should include a framework of "
                'economic abuse',
            'help_text':
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence',
            'active': True,
            'deactivated_at': None,
            'adverse': False,
        })

        criterion2_expected = {
            'id': criterion2.id,
            'category_id': criterion2.category_id,
            'title': 'Uses coercive control framework',
            'recommendation_text':
                "The state's definition of domestic violence should use a framework of coercive "
                'control',
            'help_text':
                'This means that the state acknowledges the role that coercion can play in '
                'domestic violence',
            'active': False,
            'adverse': True,
        }

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(criterion2_expected.items() <= json_response[1].items())
        self.assertTrue(isinstance(json_response[1]['deactivated_at'], str))

    def test_get_criteria_empty(self):
        response = self.client.get('/criteria')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, [])

    def test_get_criterion(self):
        criterion = Criterion(
            category_id=self.category.id,
            title='Includes economic abuse framework',
            recommendation_text=(
                "The state's definition of domestic violence should include a framework of "
                'economic abuse'
            ),
            help_text=(
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence'
            ),
            adverse=False,
        ).save()

        response = self.client.get('/criteria/%i' % criterion.id)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(json_response, {
            'id': criterion.id,
            'category_id': criterion.category_id,
            'title': 'Includes economic abuse framework',
            'recommendation_text':
                "The state's definition of domestic violence should include a framework of "
                'economic abuse',
            'help_text':
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence',
            'active': True,
            'deactivated_at': None,
            'adverse': False,
        })

    def test_get_criterion_doesnt_exist(self):
        response = self.client.get('/criteria/1')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.criterion_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_post_criterion(self, mock_auth):
        category_id = self.category.id
        data = {
            'category_id': category_id,
            'title': 'Includes economic abuse framework',
            'recommendation_text':
                "The state's definition of domestic violence should include a framework of "
                'economic abuse',
            'help_text':
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence',
            'adverse': False,
        }

        response = self.client.post('/criteria', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 201)
        mock_auth.assert_called_once()

        criterion = Criterion.query.one()
        self.assertEqual(criterion.category_id, category_id)
        self.assertEqual(criterion.title, 'Includes economic abuse framework')
        self.assertEqual(
            criterion.recommendation_text,
            "The state's definition of domestic violence should include a framework of economic "
            'abuse',
        )
        self.assertEqual(
            criterion.help_text,
            'This means that the state acknowledges the role that economic control and abuse can '
            'play in domestic violence',
        )
        self.assertFalse(criterion.adverse)
        self.assertTrue(criterion.active)
        self.assertIsNone(criterion.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, {
            'id': criterion.id,
            'category_id': category_id,
            'title': 'Includes economic abuse framework',
            'recommendation_text':
                "The state's definition of domestic violence should include a framework of "
                'economic abuse',
            'help_text':
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence',
            'adverse': False,
            'active': True,
            'deactivated_at': None,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_post_criterion_category_doesnt_exist(self, mock_auth):
        category_id = self.category.id + 1
        data = {'category_id': category_id}

        response = self.client.post('/criteria', json=data, headers=auth_headers())
        self.assertEqual(response.status_code, 404)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.category_not_found)

    def test_post_criterion_no_auth(self):
        response = self.client.post('/criteria', data={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_criterion(self, mock_auth):
        category_id = self.category.id
        criterion = create_criterion(category_id)

        data = {
            'title': 'A New Title',
            'help_text': 'Some new help text',
        }

        response = self.client.put(
            '/criteria/%i' % criterion.id,
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        criterion = Criterion.query.first()
        self.assertEqual(criterion.category_id, category_id)
        self.assertEqual(criterion.title, 'A New Title')
        self.assertEqual(
            criterion.recommendation_text,
            "The state's definition of domestic violence should include a framework of economic "
            'abuse',
        )
        self.assertEqual(criterion.help_text, 'Some new help text')
        self.assertFalse(criterion.adverse)
        self.assertTrue(criterion.active)
        self.assertIsNone(criterion.deactivated_at)

        json_response = json.loads(response.data)
        self.assertEqual(json_response, {
            'id': criterion.id,
            'category_id': category_id,
            'title': 'A New Title',
            'recommendation_text':
                "The state's definition of domestic violence should include a framework of "
                'economic abuse',
            'help_text': 'Some new help text',
            'adverse': False,
            'active': True,
            'deactivated_at': None,
        })

    @patch('auth.is_token_valid', return_value=True)
    def test_put_criterion_change_category(self, mock_auth):
        category_id = self.category.id
        criterion = create_criterion(category_id)

        data = {'category_id': category_id + 1}

        response = self.client.put(
            '/criteria/%i' % criterion.id,
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 400)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.cannot_change_category)

    def test_put_category_no_auth(self):
        response = self.client.put('/criteria/1', json={}, headers={})
        self.assertEqual(response.status_code, 401)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_criterion_doesnt_exist(self, mock_auth):
        response = self.client.put('/criteria/1', json={}, headers=auth_headers())
        self.assertEqual(response.status_code, 404)
        mock_auth.assert_called_once()

        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.criterion_not_found)

    @patch('auth.is_token_valid', return_value=True)
    def test_put_criterion_deactivate(self, mock_auth):
        criterion = create_criterion(self.category.id)

        data = {
            'active': False,
        }

        response = self.client.put(
            '/criteria/%i' % criterion.id,
            json=data,
            headers=auth_headers(),
        )
        self.assertEqual(response.status_code, 200)
        mock_auth.assert_called_once()

        criterion = Criterion.query.first()

        self.assertFalse(criterion.active)
        self.assertTrue(isinstance(criterion.deactivated_at, datetime.datetime))

        # Criterion cannot be reactivated
        deactivated_at = criterion.deactivated_at
        data = {
            'active': True,
        }

        response = self.client.put(
            '/criteria/%i' % criterion.id,
            json=data,
            headers=auth_headers(),
        )
        criterion = Criterion.query.first()
        self.assertFalse(criterion.active)
        self.assertEqual(criterion.deactivated_at, deactivated_at)
