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
    StateSubcategoryGrade,
    Subcategory,
    ResourceLink
)


class TestImport(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

    def test_import_state(self):
        # import_state assumes that categories, subcategories, and criteria have
        # already been imported
        import_categories()

        ak_path = absolute_file_path('states/AK.yml')
        import_state(ak_path)

        state = State.query.filter_by(code='AK').first()
        self.assertIsNotNone(state)

        state_grade = StateGrade.query.filter_by(state_code='AK').first()
        self.assertEqual(state_grade.grade, 1)

        state_subcategory_grades = StateSubcategoryGrade.query.all()
        self.assertEqual(len(state_subcategory_grades), 13)
        self.assertEqual(
            list(map(lambda grade: grade.grade, state_subcategory_grades)),
            [0, 0, 0, 2, 0, -1, 0, 3, 0, 0, 0, 0, 0]
        )

        subcategory1 = Subcategory.query.filter_by(title='Paid and Protected Leave').first()

        honorable_mentions = HonorableMention.query.all()
        self.assertEqual(len(honorable_mentions), 1)
        self.assertEqual(honorable_mentions[0].subcategory_id, subcategory1.id)
        self.assertEqual(honorable_mentions[0].text, 'AS § 12.61.017')
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

        subcategory2 = Subcategory.query.filter_by(title='Economic Abuse Definition').first()

        resource_links = ResourceLink.query.all()
        self.assertEqual(len(resource_links), 18)
        self.assertEqual(resource_links[0].text, 'AS § 47.17.035')
        self.assertEqual(
            resource_links[0].url,
            'http://www.akleg.gov/basis/statutes.asp#47.17.035'
        )
        self.assertEqual(resource_links[0].subcategory_id, subcategory2.id)

        criteria_met = Score.query.filter_by(state='AK', meets_criterion=True).all()
        criteria_not_met = Score.query.filter_by(state='AK', meets_criterion=False).all()
        self.assertEqual(len(criteria_met), 10)
        self.assertEqual(len(criteria_not_met), 80)

    def test_import_categories(self):
        import_categories()

        categories = Category.query.all()
        self.assertEqual(len(categories), 9)
        self.assertEqual(
            list(map(lambda category: category.title, categories)),
            [
                'Economic Abuse Definition',
                'Worker Protections',
                'Civil Remedies and Protections',
                'VOCA',
                'Safety-Net Programs',
                'Rental Protections',
                'Coerced and Fraudulent Debt',
                'Safe Banking Protections for Survivors',
                'Reimagining Public Safety Responses to GBV'
            ]
        )

        subcategories = Subcategory.query.all()
        self.assertEqual(len(subcategories), 13)
        self.assertEqual(
            list(map(lambda subcategory: subcategory.title, subcategories)),
            [
                'Economic Abuse Definition',
                'Paid and Protected Leave',
                'Safe Work Environment',
                'Unemployment Insurance',
                'Designated Tort',
                'Litigation Abuse',
                'VOCA',
                'SNAP',
                'TANF',
                'Rental Protections',
                'Coerced and Fraudulent Debt',
                'Safe Banking Protections for Survivors',
                'Reimagining Public Safety Responses to GBV'
            ]
        )

        criteria = Criterion.query.all()
        self.assertEqual(len(criteria), 90)

        # Check a few criteria
        criterion1 = Criterion.query.filter_by(
            title='IPV programs and services are reliant on criminal justice fines and fees'
        ).first()
        subcategory1 = Subcategory.query.filter_by(
            title='Reimagining Public Safety Responses to GBV'
        ).first()
        category1 = Category.query.filter_by(
            title='Reimagining Public Safety Responses to GBV'
        ).first()
        self.assertEqual(criterion1.subcategory_id, subcategory1.id)
        self.assertTrue(criterion1.adverse)
        self.assertEqual(subcategory1.category_id, category1.id)

        criterion2 = Criterion.query.filter_by(
            title='Provides exemptions or deferments from work or job training requirements'
        ).first()
        subcategory2 = Subcategory.query.filter_by(
            title='SNAP'
        ).first()
        category2 = Category.query.filter_by(
            title='Safety-Net Programs'
        ).first()
        self.assertEqual(criterion2.subcategory_id, subcategory2.id)
        self.assertFalse(criterion2.adverse)
        self.assertEqual(subcategory2.category_id, category2.id)
