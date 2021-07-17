import unittest

from app import db
from models import (
    Category,
    Criterion,
    State,
    StateGrade,
    StateCategoryGrade,
    Score,
    ResourceLink,
    HonorableMention,
    InnovativePolicyIdea
)
from data.importer import import_categories, import_states
from tests.test_utils import clear_database


class ImporterTestCase(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

    def test_import_category(self):
        category = Category(
            title='Economic Abuse Defined in State Laws',
            help_text='We cannot begin to address economic abuse...',
        ).save()

        criterion = Criterion(
            category_id=category.id,
            title='The state’s definition of intimate partner violence includes all or similar'
                  'language to the following...',
        ).save()

        json = [
            {
                'title': 'New Title',
                'help_text': 'New Help Text',
                'id': category.id,
                'active': False,
                'criteria': [
                    {
                        'id': criterion.id,
                        'title': 'Edited Criterion',
                        'adverse': True,
                        'active': False,
                    }
                ],
            },
            {
                'title': 'Paid and Protective Leave',
                'help_text': 'Survivors in the U.S. lose an estimated 8 million days of paid '
                             'work each year...',
                'id': 140,
                'active': True,
                'criteria': [
                    {
                        'id': 50,
                        'title': 'Survivors are given leave from work to deal with the '
                                 'consequences of abuse',
                        'adverse': False,
                        'active': True,
                    }
                ],
            },
        ]

        result = import_categories(json)

        self.assertEqual(len(result), 2)

        category_1 = Category.query.get(category.id)

        self.assertEqual(category_1.title, 'New Title')
        self.assertEqual(category_1.help_text, 'New Help Text')
        self.assertFalse(category_1.active)

        criterion_1 = Criterion.query.get(criterion.id)

        self.assertEqual(criterion_1.title, 'Edited Criterion')
        self.assertEqual(criterion_1.category_id, category_1.id)
        self.assertTrue(criterion_1.adverse)
        self.assertFalse(criterion_1.active)

        category_2 = Category.query.get(140)

        self.assertEqual(category_2.title, 'Paid and Protective Leave')
        self.assertEqual(
            category_2.help_text,
            'Survivors in the U.S. lose an estimated 8 million days of paid work each year...'
        )
        self.assertTrue(category_2.active)

        criterion_2 = Criterion.query.get(50)

        self.assertEqual(
            criterion_2.title,
            'Survivors are given leave from work to deal with the consequences of abuse'
        )
        self.assertEqual(criterion_2.category_id, category_2.id)
        self.assertFalse(criterion_2.adverse)
        self.assertTrue(criterion_2.active)

        self.assertEqual(len(Category.query.all()), 2)
        self.assertEqual(len(Criterion.query.all()), 2)

    def test_import_state(self):
        state = State(code='NY', name='New York').save()

        StateGrade(
            state_code='NY',
            grade=3,
        ).save()

        category_1 = Category(
            title='Economic Abuse Defined in State Laws',
            help_text='We cannot begin to address economic abuse...',
        ).save()

        category_2 = Category(
            title='Paid and Protective Leave',
            help_text='Survivors in the U.S. lose an estimated...',
        ).save()

        criterion_1 = Criterion(
            category_id=category_1.id,
            title='The state’s definition of intimate partner violence includes all or similar'
                  'language to the following...',
        ).save()

        criterion_2 = Criterion(
            category_id=category_2.id,
            title='A definition that explicitly excludes economic abuse or tactics',
            adverse=True
        ).save()

        StateCategoryGrade(
            state_code='NY',
            category_id=category_1.id,
            grade=2,
        ).save()

        Score(
            criterion_id=criterion_1.id,
            state='NY',
            meets_criterion='maybe'
        ).save()

        resource_link = ResourceLink(
            category_id=category_1.id,
            state='NY',
        ).save()

        json = [
            {
                'name': 'New York',
                'code': 'NY',
                'total': 18,
                'quote': 'I am unemployed now for 5 months...',
                'grade': '0',
                'criteria_met': [
                    {
                        'id': criterion_1.id,
                        'meets_criterion': 'yes'
                    },
                    {
                        'id': criterion_2.id,
                        'meets_criterion': 'maybe'
                    },
                ],
                'category_grades': [
                    {
                        'id': category_1.id,
                        'grade': 3
                    },
                    {
                        'id': category_2.id,
                        'grade': 0
                    }
                ],
                'resource_links': [
                    {
                        'id': resource_link.id,
                        'state': 'NY',
                        'category_id': category_2.id,
                        'text': 'NY S.O.S. §459-a',
                        'url': 'https://www.nysenate.gov/legislation/laws/SOS/459-A',
                        'active': False
                    },
                    {
                        'id': 500,
                        'state': 'NY',
                        'category_id': category_1.id,
                        'text': 'NY E.X.C. §296(c)(1), (2)(i--v), (5)(i-iv)',
                        'url': 'https://www.nysenate.gov/legislation/laws/EXC/296',
                        'active': True
                    }
                ],
                'honorable_mentions': [
                    {
                        'id': 501,
                        'state': 'NY',
                        'category_id': category_1.id,
                        'text': 'NY SNAP website',
                        'url': 'https://www.ny.gov/services/apply-snap',
                        'description': 'In New York, expedited enrollment...',
                        'active': True
                    },
                ],
                'innovative_policy_ideas': [
                    {
                        'id': 502,
                        'state': 'NY',
                        'category_id': category_2.id,
                        'text': 'An innovative policy',
                        'url': 'https://www.ny.gov/innovative-policy',
                        'description': 'A new innovative policy for NY...',
                        'active': True
                    },
                ],
            }
        ]

        import_states(json)

        state = State.query.get('NY')
        self.assertEqual(state.total, 18)
        self.assertEqual(state.quote, 'I am unemployed now for 5 months...')

        state_grades = StateGrade.query.filter_by(state_code='NY').all()
        self.assertEqual(len(state_grades), 2)
        self.assertEqual(state_grades[1].grade, 0)

        scores = Score.query.filter_by(state='NY').all()
        self.assertEqual(len(scores), 3)

        score_1 = Score.query.filter_by(state='NY', criterion_id=criterion_1.id) \
            .order_by(Score.created_at.desc()).first()
        self.assertEqual(score_1.meets_criterion, 'yes')

        score_2 = Score.query.filter_by(state='NY', criterion_id=criterion_2.id) \
            .order_by(Score.created_at.desc()).first()
        self.assertEqual(score_2.meets_criterion, 'maybe')

        category_grades = StateCategoryGrade.query.filter_by(state_code='NY').all()
        self.assertEqual(len(category_grades), 3)

        category_grade_1 = StateCategoryGrade.query \
            .filter_by(state_code='NY', category_id=category_1.id) \
            .order_by(StateCategoryGrade.created_at.desc()).first()
        self.assertEqual(category_grade_1.grade, 3)

        category_grade_2 = StateCategoryGrade.query \
            .filter_by(state_code='NY', category_id=category_2.id) \
            .order_by(StateCategoryGrade.created_at.desc()).first()
        self.assertEqual(category_grade_2.grade, 0)

        resource_links = ResourceLink.query.filter_by(state='NY').all()
        self.assertEqual(len(resource_links), 2)
        self.assertEqual(resource_links[0].text, 'NY S.O.S. §459-a')
        self.assertEqual(
            resource_links[0].url,
            'https://www.nysenate.gov/legislation/laws/SOS/459-A'
        )
        self.assertFalse(resource_links[0].active)
        self.assertEqual(resource_links[1].text, 'NY E.X.C. §296(c)(1), (2)(i--v), (5)(i-iv)')
        self.assertEqual(
            resource_links[1].url,
            'https://www.nysenate.gov/legislation/laws/EXC/296'
        )
        self.assertTrue(resource_links[1].active)

        honorable_mentions = HonorableMention.query.filter_by(state='NY').all()
        self.assertEqual(len(honorable_mentions), 1)
        self.assertEqual(honorable_mentions[0].id, 501)
        self.assertEqual(honorable_mentions[0].text, 'NY SNAP website')
        self.assertEqual(honorable_mentions[0].url, 'https://www.ny.gov/services/apply-snap')
        self.assertEqual(
            honorable_mentions[0].description,
            'In New York, expedited enrollment...'
        )
        self.assertTrue(honorable_mentions[0].active)

        innovative_policy_ideas = InnovativePolicyIdea.query.filter_by(state='NY').all()
        self.assertEqual(len(innovative_policy_ideas), 1)
        self.assertEqual(innovative_policy_ideas[0].id, 502)
        self.assertEqual(innovative_policy_ideas[0].text, 'An innovative policy')
        self.assertEqual(innovative_policy_ideas[0].url, 'https://www.ny.gov/innovative-policy')
        self.assertEqual(
            innovative_policy_ideas[0].description,
            'A new innovative policy for NY...'
        )
        self.assertTrue(innovative_policy_ideas[0].active)
