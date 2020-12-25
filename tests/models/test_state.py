import unittest
from datetime import datetime, timedelta

from app import app, db
from models import State, Score
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    create_subcategory,
    create_criterion,
    create_link,
)


class StateTestCase(unittest.TestCase):
    def setUp(self):
        clear_database(db)
        self.client = app.test_client()
        self.state1 = State(
            code='NY',
            name='New York',
            innovative_idea='Innovative idea',
            honorable_mention='Honorable mention',
        ).save()
        self.state2 = create_state(code='AZ')
        self.category = create_category()
        self.subcategory = create_subcategory(self.category.id)
        self.criterion1 = create_criterion(self.subcategory.id)
        self.criterion2 = create_criterion(self.subcategory.id)
        self.link1 = create_link(
            subcategory_id=self.subcategory.id,
            state=self.state1.code,
        )
        self.link2 = create_link(
            subcategory_id=self.subcategory.id,
            state=self.state1.code,
        )
        self.score1 = Score(
            criterion_id=self.criterion1.id,
            state=self.state1.code,
            meets_criterion=True,
        )
        self.score2 = Score(
            criterion_id=self.criterion2.id,
            state=self.state1.code,
            meets_criterion=False,
        )
        self.score3 = Score(
            criterion_id=self.criterion2.id,
            state=self.state1.code,
            meets_criterion=True,
        )
        # score2 is more recent than score3
        self.score3.created_at = datetime.utcnow() - timedelta(5)
        self.score4 = Score(
            criterion_id=self.criterion2.id,
            state=self.state2.code,
            meets_criterion=True,
        )

        Score.save_all([self.score1, self.score2, self.score3, self.score4])
        self.maxDiff = None

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.state1.code, 'NY')
        self.assertEqual(self.state1.name, 'New York')
        self.assertEqual(self.state1.innovative_idea, 'Innovative idea')
        self.assertEqual(self.state1.honorable_mention, 'Honorable mention')

    def test_serialize(self):
        self.assertEqual(
            {
                'code': 'NY',
                'name': 'New York',
                'innovative_idea': 'Innovative idea',
                'honorable_mention': 'Honorable mention',
                'links': [
                    self.link1.serialize(),
                    self.link2.serialize(),
                ],
                'scores': [
                    self.score1.serialize(),
                    self.score2.serialize(),
                ]
            },
            self.state1.serialize()
        )
