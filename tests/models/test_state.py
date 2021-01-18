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
    create_state_grade,
    create_state_category_grade,
    create_resource_link,
)


class StateTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.state = State(
            code='NY',
            name='New York',
            innovative_idea='Innovative idea',
            honorable_mention='Honorable mention',
        ).save()
        other_state = create_state(code='AZ')

        category1 = create_category()
        category2 = create_category()
        subcategory = create_subcategory(category1.id)
        criterion1 = create_criterion(subcategory.id)
        criterion2 = create_criterion(subcategory.id)

        self.link1 = create_resource_link(subcategory.id, self.state.code)
        self.link2 = create_resource_link(subcategory.id, self.state.code)

        self.state_grade1 = create_state_grade(self.state.code)
        self.state_grade2 = create_state_grade(self.state.code)

        # state_grade1 is more recent than state_grade2
        self.state_grade1.created_at = datetime.utcnow()
        self.state_grade2.created_at = datetime.utcnow() - timedelta(5)

        self.state_category_grade1 = create_state_category_grade(self.state.code, category1.id)
        self.state_category_grade2 = create_state_category_grade(self.state.code, category1.id)
        self.state_category_grade3 = create_state_category_grade(self.state.code, category2.id)

        # state_category_grade1 is more recent than state_category_grade2
        self.state_category_grade1.created_at = datetime.utcnow()
        self.state_category_grade2.created_at = datetime.utcnow() - timedelta(5)

        self.score1 = Score(
            criterion_id=criterion1.id,
            state=self.state.code,
            meets_criterion=True,
        )
        self.score2 = Score(
            criterion_id=criterion2.id,
            state=self.state.code,
            meets_criterion=False,
        )
        self.score3 = Score(
            criterion_id=criterion2.id,
            state=self.state.code,
            meets_criterion=True,
        )
        # score2 is more recent than score3
        self.score3.created_at = datetime.utcnow() - timedelta(5)
        self.score4 = Score(
            criterion_id=criterion2.id,
            state=other_state.code,
            meets_criterion=True,
        )

        Score.save_all([self.score1, self.score2, self.score3, self.score4])
        self.maxDiff = None

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.state.code, 'NY')
        self.assertEqual(self.state.name, 'New York')
        self.assertEqual(self.state.innovative_idea, 'Innovative idea')
        self.assertEqual(self.state.honorable_mention, 'Honorable mention')

    def test_serialize(self):
        self.assertEqual(
            {
                'code': 'NY',
                'name': 'New York',
                'innovative_idea': 'Innovative idea',
                'honorable_mention': 'Honorable mention',
                'grade': self.state_grade1.serialize(),
                'category_grades': [
                    self.state_category_grade1.serialize(),
                    self.state_category_grade3.serialize(),
                ],
                'criterion_scores': [
                    self.score1.serialize(),
                    self.score2.serialize(),
                ],
                'resource_links': [
                    self.link1.serialize(),
                    self.link2.serialize(),
                ],
            },
            self.state.serialize()
        )

    def test_serialize_no_grades(self):
        state = create_state(code='AK')
        self.assertEqual(
            {
                'code': state.code,
                'name': state.name,
                'innovative_idea': state.innovative_idea,
                'honorable_mention': state.honorable_mention,
                'grade': None,
                'category_grades': [],
                'criterion_scores': [],
                'resource_links': [],
            },
            state.serialize()
        )
