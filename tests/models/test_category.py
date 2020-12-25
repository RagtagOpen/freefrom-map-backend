import unittest
import datetime

from app import app, db
from models import Category
from tests.test_utils import clear_database, create_subcategory


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.category = Category(
            title='Definition of Domestic Violence',
            help_text="This is how a state legally defines the term 'domestic violence'",
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.category.title, 'Definition of Domestic Violence')
        self.assertEqual(
            self.category.help_text,
            "This is how a state legally defines the term 'domestic violence'",
        )
        self.assertTrue(self.category.active)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.category.id,
                'title': 'Definition of Domestic Violence',
                'help_text': "This is how a state legally defines the term 'domestic violence'",
                'active': True,
                'deactivated_at': None,
            },
            self.category.serialize()
        )

    def test_serialize_with_subcategories(self):
        subcategory1 = create_subcategory(self.category.id)
        subcategory2 = create_subcategory(self.category.id)
        self.assertEqual(
            {
                'id': self.category.id,
                'title': 'Definition of Domestic Violence',
                'help_text': "This is how a state legally defines the term 'domestic violence'",
                'active': True,
                'deactivated_at': None,
                'subcategories': [
                    subcategory1.serialize(),
                    subcategory2.serialize(),
                ]
            },
            self.category.serialize(with_subcategories=True)
        )

    def test_deactivate(self):
        self.category.deactivate()

        self.assertFalse(self.category.active)
        self.assertTrue(isinstance(self.category.deactivated_at, datetime.datetime))
        self.assertTrue(self.category.deactivated_at < datetime.datetime.utcnow())
