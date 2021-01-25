import unittest
import datetime

from app import db
from models import StateSubcategoryGrade
from strings import invalid_state, subcategory_not_found, invalid_grade
from tests.test_utils import clear_database, create_state, create_category, create_subcategory


class StateSubcategoryGradeTestCase(unittest.TestCase):
    def setUp(self):
        self.state = create_state()
        self.category = create_category()
        self.subcategory = create_subcategory(self.category.id)
        self.grade = StateSubcategoryGrade(
            state_code=self.state.code,
            subcategory_id=self.subcategory.id,
            grade=2,
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.grade.state_code, self.state.code)
        self.assertEqual(self.grade.subcategory_id, self.subcategory.id)
        self.assertTrue(self.grade.grade, 2)
        self.assertTrue(isinstance(self.grade.created_at, datetime.datetime))
        self.assertTrue(self.grade.created_at < datetime.datetime.utcnow())

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            StateSubcategoryGrade(
                state_code='fake-state-code',
                subcategory_id=self.subcategory.id,
                grade=2,
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_init_invalid_subcategory_id(self):
        with self.assertRaises(ValueError) as e:
            StateSubcategoryGrade(
                state_code=self.state.code,
                subcategory_id=0,
                grade=2,
            )
        self.assertEqual(str(e.exception), subcategory_not_found)

    def test_init_invalid_grade(self):
        with self.assertRaises(ValueError) as e:
            StateSubcategoryGrade(
                state_code=self.state.code,
                subcategory_id=self.subcategory.id,
                grade=-2,
            )
        self.assertEqual(str(e.exception), invalid_grade)

        with self.assertRaises(ValueError) as e:
            StateSubcategoryGrade(
                state_code=self.state.code,
                subcategory_id=self.subcategory.id,
                grade=4,
            )
        self.assertEqual(str(e.exception), invalid_grade)

    def test_serialize(self):
        expected_result = {
            'id': self.grade.id,
            'state_code': self.state.code,
            'subcategory_id': self.subcategory.id,
            'grade': 2,
        }

        self.assertEqual(self.grade.serialize(), expected_result)
