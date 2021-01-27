import unittest
import datetime

from app import app, db
from models import Category
from tests.test_utils import clear_database, create_criterion


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = Category(
            title='Safe Work Environment',
            help_text='Some help text',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.category.title, 'Safe Work Environment')
        self.assertEqual(self.category.help_text, 'Some help text')
        self.assertTrue(self.category.active)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.category.id,
                'title': 'Safe Work Environment',
                'help_text': 'Some help text',
                'active': True,
                'deactivated_at': None,
            },
            self.category.serialize()
        )

    def test_serialize_with_criteria(self):
        criterion1 = create_criterion(self.category.id)
        criterion2 = create_criterion(self.category.id)
        self.assertEqual(
            {
                'id': self.category.id,
                'title': 'Safe Work Environment',
                'help_text': 'Some help text',
                'active': True,
                'deactivated_at': None,
                'criteria': [
                    criterion1.serialize(),
                    criterion2.serialize(),
                ]
            },
            self.category.serialize(with_criteria=True)
        )

    def test_deactivate(self):
        self.category.deactivate()

        self.assertFalse(self.category.active)
        self.assertTrue(isinstance(self.category.deactivated_at, datetime.datetime))
        self.assertTrue(self.category.deactivated_at < datetime.datetime.utcnow())
