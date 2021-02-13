import unittest
import datetime

from app import db
from models import Score
from strings import criterion_not_found, invalid_state, invalid_meets_criterion
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    create_criterion,
)


class ScoreTestCase(unittest.TestCase):
    def setUp(self):
        self.state = create_state()
        self.category = create_category()
        self.criterion = create_criterion(self.category.id)
        self.score = Score(
            criterion_id=self.criterion.id,
            state=self.state.code,
            meets_criterion='yes',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.score.criterion_id, self.criterion.id)
        self.assertEqual(self.score.state, self.state.code)
        self.assertEqual(self.score.meets_criterion, 'yes')
        self.assertTrue(isinstance(self.score.created_at, datetime.datetime))
        self.assertTrue(self.score.created_at < datetime.datetime.utcnow())

    def test_init_does_not_meet_criterion(self):
        score = Score(
            criterion_id=self.criterion.id,
            state=self.state.code,
            meets_criterion='no',
        ).save()
        self.assertEqual(score.meets_criterion, 'no')

    def test_init_maybe_meets_criterion(self):
        score = Score(
            criterion_id=self.criterion.id,
            state=self.state.code,
            meets_criterion='maybe',
        ).save()
        self.assertEqual(score.meets_criterion, 'maybe')

    def test_init_invalid_criterion(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=0,
                state=self.state.code,
                meets_criterion='yes',
            )
        self.assertEqual(str(e.exception), criterion_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=self.criterion.id,
                state='fake-state',
                meets_criterion='yes',
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_init_invalid_meets_criterion(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=self.criterion.id,
                state=self.state.code,
                meets_criterion='blah',
            )
        self.assertEqual(str(e.exception), invalid_meets_criterion)

    def test_serialize(self):
        expected_result = {
            'id': self.score.id,
            'criterion_id': self.criterion.id,
            'state': self.state.code,
            'meets_criterion': 'yes',
        }

        actual_result = self.score.serialize()

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(expected_result.items() <= actual_result.items())
