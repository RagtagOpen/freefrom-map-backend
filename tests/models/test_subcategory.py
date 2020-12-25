import unittest
import datetime

from app import app, db
from models import Subcategory
from tests.test_utils import clear_database, create_category, create_criterion


class SubcategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = create_category()
        self.subcategory = Subcategory(
            category_id=self.category.id,
            title='Safe Work Environment',
            help_text='Some help text',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.subcategory.category_id, self.category.id)
        self.assertEqual(self.subcategory.title, 'Safe Work Environment')
        self.assertEqual(self.subcategory.help_text, 'Some help text')
        self.assertTrue(self.subcategory.active)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.subcategory.id,
                'category_id': self.category.id,
                'title': 'Safe Work Environment',
                'help_text': 'Some help text',
                'active': True,
                'deactivated_at': None,
            },
            self.subcategory.serialize()
        )

    def test_serialize_with_criteria(self):
        criterion1 = create_criterion(self.subcategory.id)
        criterion2 = create_criterion(self.subcategory.id)
        self.assertEqual(
            {
                'id': self.subcategory.id,
                'category_id': self.category.id,
                'title': 'Safe Work Environment',
                'help_text': 'Some help text',
                'active': True,
                'deactivated_at': None,
                'criteria': [
                    criterion1.serialize(),
                    criterion2.serialize(),
                ]
            },
            self.subcategory.serialize(with_criteria=True)
        )

    def test_deactivate(self):
        self.subcategory.deactivate()

        self.assertFalse(self.subcategory.active)
        self.assertTrue(isinstance(self.subcategory.deactivated_at, datetime.datetime))
        self.assertTrue(self.subcategory.deactivated_at < datetime.datetime.utcnow())
