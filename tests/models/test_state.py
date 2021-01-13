import unittest
from datetime import datetime, timedelta

from app import app, db
from models import State, Score, CategoryLink
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    create_subcategory,
    create_criterion,
    create_state_grade,
    create_state_category_grade,
    create_link,
)


class StateTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.state = State(
            code='NY',
            name='New York',
        ).save()
        other_state = create_state(code='AZ')

        category1 = create_category()
        category2 = create_category()
        subcategory = create_subcategory(category1.id)
        criterion1 = create_criterion(subcategory.id)
        criterion2 = create_criterion(subcategory.id)

        self.link1 = create_link(subcategory.id, self.state.code)
        self.link2 = create_link(subcategory.id, self.state.code)

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

        self.category_link1 = CategoryLink(
            category_id=category1.id,
            state=self.state.code,
            type='innovative_policy_idea'
        )
        self.category_link2 = CategoryLink(
            category_id=category1.id,
            state=self.state.code,
            type='honorable_mention'
        )
        self.category_link3 = CategoryLink(
            category_id=category2.id,
            state=self.state.code,
            type='honorable_mention'
        )
        self.category_link4 = CategoryLink(
            category_id=category2.id,
            state=self.state.code,
            type='honorable_mention'
        )
        # category_link3 was created more recently than category_link4
        self.category_link4.created_at = datetime.utcnow() - timedelta(5)
        self.category_link5 = CategoryLink(
            category_id=category1.id,
            state=other_state.code,
            type='honorable_mention'
        )

        CategoryLink.save_all([
            self.category_link1,
            self.category_link2,
            self.category_link3,
            self.category_link4,
            self.category_link5
        ])

        self.maxDiff = None

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.state.code, 'NY')
        self.assertEqual(self.state.name, 'New York')

    def test_serialize(self):
        self.assertEqual(
            {
                'code': 'NY',
                'name': 'New York',
                'grade': self.state_grade1.serialize(),
                'category_grades': [
                    self.state_category_grade1.serialize(),
                    self.state_category_grade3.serialize(),
                ],
                'criterion_scores': [
                    self.score1.serialize(),
                    self.score2.serialize(),
                ],
                'links': [
                    self.link1.serialize(),
                    self.link2.serialize(),
                ],
                'category_links': [
                    self.category_link1.serialize(),
                    self.category_link2.serialize(),
                    self.category_link3.serialize(),
                ]
            },
            self.state.serialize()
        )

    def test_serialize_no_grades(self):
        state = create_state(code='AK')
        self.assertEqual(
            {
                'code': state.code,
                'name': state.name,
                'grade': None,
                'category_grades': [],
                'criterion_scores': [],
                'links': [],
                'category_links': []
            },
            state.serialize()
        )
