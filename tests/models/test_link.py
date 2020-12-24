import unittest
import datetime

from app import db
from models import Link
from strings import category_not_found, invalid_state
from tests.test_utils import clear_database, create_state, create_category


class LinkTestCase(unittest.TestCase):
    def setUp(self):
        self.state = 'NY'
        create_state(code=self.state)
        self.category = create_category()
        self.link = Link(
            category_id=self.category.id,
            state=self.state,
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.link.category_id, self.category.id)
        self.assertEqual(self.link.state, self.state)
        self.assertEqual(self.link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(self.link.url, 'ny.gov/link/to/statute')
        self.assertTrue(self.category.active)

    def test_init_invalid_category(self):
        with self.assertRaises(ValueError) as e:
            Link(
                category_id=0,
                state=self.state,
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), category_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            Link(
                category_id=self.category.id,
                state='fake-state',
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.link.id,
                'category_id': self.category.id,
                'state': self.state,
                'text': 'Section 20 of Statute 39-B',
                'url': 'ny.gov/link/to/statute',
                'active': True,
                'deactivated_at': None,
            },
            self.link.serialize()
        )

    def test_deactivate(self):
        self.link.deactivate()

        self.assertFalse(self.link.active)
        self.assertTrue(isinstance(self.link.deactivated_at, datetime.datetime))
        self.assertTrue(self.link.deactivated_at < datetime.datetime.utcnow())
