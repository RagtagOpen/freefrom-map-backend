import unittest
import datetime

from app import db
from models import Score
from strings import criterion_not_found, invalid_state
from tests.test_utils import clear_database, create_category, create_criterion


class ScoreTestCase(unittest.TestCase):
    def setUp(self):
        self.category = create_category()
        self.criterion = create_criterion(self.category.id)
        self.score = Score(
            criterion_id=self.criterion.id,
            state='NY',
            meets_criterion=True,
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.score.criterion_id, self.criterion.id)
        self.assertEqual(self.score.state, 'NY')
        self.assertTrue(self.score.meets_criterion)
        self.assertTrue(isinstance(self.score.created_at, datetime.datetime))
        self.assertTrue(self.score.created_at < datetime.datetime.utcnow())

    def test_init_invalid_criterion(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=0,
                state='NY',
                meets_criterion=True,
            )
        self.assertEqual(str(e.exception), criterion_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=self.criterion.id,
                state='fake-state',
                meets_criterion=True,
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        expected_result = {
            'id': self.score.id,
            'criterion_id': self.criterion.id,
            'state': 'NY',
            'meets_criterion': True,
        }

        actual_result = self.score.serialize()

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(expected_result.items() <= actual_result.items())
