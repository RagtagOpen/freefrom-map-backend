import unittest
import datetime

from app import db
from models import StateGrade
from strings import invalid_state, invalid_grade
from tests.test_utils import clear_database, create_state


class StateGradeTestCase(unittest.TestCase):
    def setUp(self):
        self.state = create_state()
        self.grade = StateGrade(
            state_code=self.state.code,
            grade=2,
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.grade.state_code, self.state.code)
        self.assertTrue(self.grade.grade, 2)
        self.assertTrue(isinstance(self.grade.created_at, datetime.datetime))
        self.assertTrue(self.grade.created_at < datetime.datetime.utcnow())

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            StateGrade(
                state_code='fake-state-code',
                grade=2,
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_init_invalid_grade(self):
        with self.assertRaises(ValueError) as e:
            StateGrade(
                state_code=self.state.code,
                grade=-2,
            )
        self.assertEqual(str(e.exception), invalid_grade)

        with self.assertRaises(ValueError) as e:
            StateGrade(
                state_code=self.state.code,
                grade=4,
            )
        self.assertEqual(str(e.exception), invalid_grade)

    def test_serialize(self):
        expected_result = {
            'id': self.grade.id,
            'state_code': self.state.code,
            'grade': 2,
        }

        self.assertEqual(self.grade.serialize(), expected_result)
