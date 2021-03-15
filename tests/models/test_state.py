import unittest
from datetime import datetime, timedelta

from app import app, db
from models import State, Score, HonorableMention, InnovativePolicyIdea
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
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
            total=34,
        ).save()
        other_state = create_state(code='AZ')

        category = create_category()
        category2 = create_category()
        criterion1 = create_criterion(category.id)
        criterion2 = create_criterion(category.id)

        self.link1 = create_resource_link(category.id, self.state.code)
        self.link2 = create_resource_link(category.id, self.state.code)

        self.state_grade1 = create_state_grade(self.state.code)
        self.state_grade2 = create_state_grade(self.state.code)

        # state_grade1 is more recent than state_grade2
        self.state_grade1.created_at = datetime.utcnow()
        self.state_grade2.created_at = datetime.utcnow() - timedelta(5)

        self.state_category_grade1 = create_state_category_grade(
            self.state.code,
            category.id
        )
        self.state_category_grade2 = create_state_category_grade(
            self.state.code,
            category.id
        )
        self.state_category_grade3 = create_state_category_grade(
            self.state.code,
            category2.id
        )

        # state_category_grade1 is more recent than state_category_grade2
        self.state_category_grade1.created_at = datetime.utcnow()
        self.state_category_grade2.created_at = datetime.utcnow() - timedelta(5)

        self.score1 = Score(
            criterion_id=criterion1.id,
            state=self.state.code,
            meets_criterion='yes',
        )
        self.score2 = Score(
            criterion_id=criterion2.id,
            state=self.state.code,
            meets_criterion='no',
        )
        self.score3 = Score(
            criterion_id=criterion2.id,
            state=self.state.code,
            meets_criterion='yes',
        )
        # score2 is more recent than score3
        self.score3.created_at = datetime.utcnow() - timedelta(5)
        self.score4 = Score(
            criterion_id=criterion2.id,
            state=other_state.code,
            meets_criterion='maybe',
        )

        Score.save_all([self.score1, self.score2, self.score3, self.score4])

        self.innovative_policy_idea1 = InnovativePolicyIdea(
            category_id=category.id,
            state=self.state.code,
        )
        self.honorable_mention1 = HonorableMention(
            category_id=category.id,
            state=self.state.code,
        )
        self.honorable_mention2 = HonorableMention(
            category_id=category2.id,
            state=self.state.code,
        )
        self.honorable_mention3 = HonorableMention(
            category_id=category2.id,
            state=self.state.code,
        )
        # honorable_mention2 was created more recently than honorable_mention3
        self.honorable_mention3.created_at = datetime.utcnow() - timedelta(5)
        self.honorable_mention4 = HonorableMention(
            category_id=category.id,
            state=other_state.code,
        )
        self.innovative_policy_idea2 = InnovativePolicyIdea(
            category_id=category.id,
            state=self.state.code,
        )
        self.innovative_policy_idea2.deactivate()

        HonorableMention.save_all([
            self.honorable_mention1,
            self.honorable_mention2,
            self.honorable_mention3,
            self.honorable_mention4,
        ])

        InnovativePolicyIdea.save_all([
            self.innovative_policy_idea1,
            self.innovative_policy_idea2,
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
                'total': 34,
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
                'honorable_mentions': [
                    self.honorable_mention1.serialize(),
                    self.honorable_mention2.serialize(),
                ],
                'innovative_policy_ideas': [
                    self.innovative_policy_idea1.serialize(),
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
                'total': 0,
                'grade': None,
                'category_grades': [],
                'criterion_scores': [],
                'honorable_mentions': [],
                'innovative_policy_ideas': [],
                'resource_links': [],
            },
            state.serialize()
        )
