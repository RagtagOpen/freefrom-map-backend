import unittest

from app import db
from tests.test_utils import clear_database
from data.imports import import_categories
from models import Category, Subcategory, Criterion


class TestImport(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

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
