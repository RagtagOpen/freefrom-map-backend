import unittest
import json

from app import app, db
import strings
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    create_state_grade,
    create_state_category_grade,
)


class GradesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.state = create_state()
        category = create_category()
        create_state_grade(self.state.code)
        create_state_grade(self.state.code)
        create_state_category_grade(self.state.code, category.id)
        create_state_category_grade(self.state.code, category.id)

    def tearDown(self):
        clear_database(db)

    def test_get_state_grades(self):
        expected_result = {
            'grade': self.state.serialize()['grade'],
            'category_grades': self.state.serialize()['category_grades'],
        }
        response = self.client.get(f'/grades/{self.state.code}')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data)
        self.assertEqual(json_response, expected_result)

    def test_get_state_grades_state_doesnt_exist(self):
        response = self.client.get('/states/PP')
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['description'], strings.invalid_state)
