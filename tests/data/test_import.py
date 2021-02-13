import unittest

from app import db
from tests.test_utils import clear_database
from data.import_data import import_categories, import_state, absolute_file_path
from models import (
    Category,
    Criterion,
    HonorableMention,
    InnovativePolicyIdea,
    Score,
    State,
    StateGrade,
    StateCategoryGrade,
    ResourceLink
)


class TestImport(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

    def test_import_state(self):
        # import_state assumes that categories and criteria have
        # already been imported
        import_categories()

        ak_path = absolute_file_path('states/AK.yml')
        import_state(ak_path)

        state = State.query.filter_by(code='AK').first()
        self.assertIsNotNone(state)

        state_grade = StateGrade.query.filter_by(state_code='AK').first()
        self.assertEqual(state_grade.grade, -1)

        state_category_grades = StateCategoryGrade.query.all()
        self.assertEqual(len(state_category_grades), 13)
        self.assertEqual(
            list(map(lambda grade: grade.grade, state_category_grades)),
            [0, 0, 0, 2, 0, 0, -1, 0, 3, 0, 0, 0, -1]
        )

        category1 = Category.query.filter_by(title='Paid and Protective Leave').first()

        honorable_mentions = HonorableMention.query.all()
        self.assertEqual(len(honorable_mentions), 1)
        self.assertEqual(honorable_mentions[0].category_id, category1.id)
        self.assertEqual(honorable_mentions[0].text, 'AS 12.61.017')
        self.assertEqual(
            honorable_mentions[0].url,
            'http://www.akleg.gov/basis/statutes.asp#12.61.017'
        )
        self.assertEqual(
            honorable_mentions[0].description,
            'Victims of crimes are granted protections from employer penalization if the ' +
            'victim is subpoenaed or requested by the prosecuting attorney to attend a ' +
            'court proceeding for the purpose of giving testimony, needs to report the ' +
            'crime to law enforcement or participates in an investigation of the offense.'
        )

        innovative_policy_ideas = InnovativePolicyIdea.query.all()
        self.assertEqual(len(innovative_policy_ideas), 0)

        category2 = Category.query.filter_by(title='Economic Abuse Defined in State Laws').first()

        resource_links = ResourceLink.query.all()
        self.assertEqual(len(resource_links), 19)
        self.assertEqual(resource_links[0].text, 'AS 47.17.035')
        self.assertEqual(
            resource_links[0].url,
            'http://www.akleg.gov/basis/statutes.asp#47.17.035'
        )
        self.assertEqual(resource_links[0].category_id, category2.id)

        criteria_met = Score.query.filter_by(state='AK', meets_criterion='yes').all()
        criteria_not_met = Score.query.filter_by(state='AK', meets_criterion='no').all()
        self.assertEqual(len(criteria_met), 13)
        self.assertEqual(len(criteria_not_met), 69)

    def test_import_categories(self):
        import_categories()

        categories = Category.query.all()
        self.assertEqual(len(categories), 13)
        self.assertEqual(
            list(map(lambda category: category.title, categories)),
            [
                'Economic Abuse Defined in State Laws',
                'Paid and Protective Leave',
                'Safe Workplaces',
                'Unemployment Insurance (UI) Accessibility',
                'Litigation Abuse Protections',
                'Designated Tort for Intimate Partner Violence',
                'Victims of Crime Compensation Accessibility',
                'Supplemental Nutrition Assistance Program (SNAP) Accessibility',
                'Temporary Assistance for Needy Families (TANF) Accessibility',
                'Safe Banking Protections',
                'Coerced and Fraudulent Debt Protections',
                'Rental Protections',
                'Alternatives to Law Enforcement Responses'
            ]
        )

        criteria = Criterion.query.all()
        self.assertEqual(len(criteria), 82)

        # Check a few criteria
        criterion1 = Criterion.query.filter_by(
            title='Mandatory arrest requirements for calls related to intimate partner violence'
        ).first()
        category1 = Category.query.filter_by(
            title='Alternatives to Law Enforcement Responses'
        ).first()
        self.assertEqual(
            category1.help_text,
            'Survivor experiences and research shows that involving law enforcement ' +
            'in responses to intimate partner violence can cause more harm to ' +
            'survivors and their families. Survivors should be able to decide when ' +
            'and how they want to involve law enforcement. See our recent statement ' +
            'for more information on this topic.'
        )
        self.assertEqual(criterion1.category_id, category1.id)
        self.assertTrue(criterion1.adverse)

        criterion2 = Criterion.query.filter_by(
            title='Survivors are eligible for expedited enrollment into the program'
        ).first()
        category2 = Category.query.filter_by(
            title='Supplemental Nutrition Assistance Program (SNAP) Accessibility'
        ).first()
        self.assertEqual(criterion2.category_id, category2.id)
        self.assertFalse(criterion2.adverse)
