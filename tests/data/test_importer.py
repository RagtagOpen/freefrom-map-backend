import unittest

from app import db
from models import Category, Criterion
from data.importer import import_categories
from tests.test_utils import clear_database


class ImporterTestCase(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

    def test_import_new_category(self):
        json = [{
            'title': 'Economic Abuse Defined in State Laws',
            'help_text': 'We cannot begin to address economic abuse...',
            'id': 140,
            'criteria': [],
        }]

        result = import_categories(json)

        self.assertEqual(len(result), 1)

        category = result[0]

        self.assertEqual(category['id'], 140)
        self.assertEqual(category['title'], 'Economic Abuse Defined in State Laws')
        self.assertEqual(category['help_text'], 'We cannot begin to address economic abuse...')
        self.assertTrue(category['active'])

        self.assertEqual(len(Category.query.all()), 1)

    def test_update_existing_category(self):
        category = Category(
            title='Economic Abuse Defined in State Laws',
            help_text='We cannot begin to address economic abuse...',
        ).save()

        json = [{
            'title': 'New Title',
            'help_text': 'New Help Text',
            'id': category.id,
            'active': False,
            'criteria': [],
        }]

        result = import_categories(json)

        self.assertEqual(len(result), 1)

        category = result[0]

        self.assertEqual(category['title'], 'New Title')
        self.assertEqual(category['help_text'], 'New Help Text')
        self.assertFalse(category['active'])

        self.assertEqual(len(Category.query.all()), 1)

    def test_new_and_existing_category(self):
        category = Category(
            title='Economic Abuse Defined in State Laws',
            help_text='We cannot begin to address economic abuse...',
        ).save()

        json = [
            {
                'title': 'New Title',
                'help_text': 'New Help Text',
                'id': category.id,
                'active': False,
                'criteria': [],
            },
            {
                'title': 'Economic Abuse Defined in State Laws',
                'help_text': 'We cannot begin to address economic abuse...',
                'id': 140,
                'criteria': [],
            },
        ]

        result = import_categories(json)

        self.assertEqual(len(result), 2)

        category_1 = result[0]

        self.assertEqual(category_1['id'], category.id)
        self.assertEqual(category_1['title'], 'New Title')
        self.assertEqual(category_1['help_text'], 'New Help Text')
        self.assertFalse(category_1['active'])

        category_2 = result[1]

        self.assertEqual(category_2['id'], 140)
        self.assertEqual(category_2['title'], 'Economic Abuse Defined in State Laws')
        self.assertEqual(category_2['help_text'], 'We cannot begin to address economic abuse...')
        self.assertTrue(category_2['active'])

        self.assertEqual(len(Category.query.all()), 2)
