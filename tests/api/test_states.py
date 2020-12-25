import unittest
import json

from app import app, db
from models import State
import strings
from tests.test_utils import clear_database


class StatesTestCase(unittest.TestCase):
    def setUp(self):
        clear_database(db)
        self.client = app.test_client()

    def tearDown(self):
        clear_database(db)

    def test_get_state(self):
        state = State(
            code='NY',
            name='New York',
            innovative_idea='Innovative idea',
            honorable_mention='Honorable mention',
        ).save()
        response = self.client.get(f'/states/{state.code}')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data)
        self.assertEqual(json_response, state.serialize())

    def test_get_state_doesnt_exist(self):
        response = self.client.get('/states/PP')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.invalid_state)
