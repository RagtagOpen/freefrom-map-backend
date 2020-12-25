import unittest
import datetime

from app import db
from models import Link
from strings import subcategory_not_found, invalid_state
from tests.test_utils import clear_database, create_state, create_category, create_subcategory


class LinkTestCase(unittest.TestCase):
    def setUp(self):
        self.state_code = 'NY'
        create_state(code=self.state_code)
        self.category = create_category()
        self.subcategory = create_subcategory(self.category.id)
        self.link = Link(
            subcategory_id=self.subcategory.id,
            state=self.state_code,
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.link.subcategory_id, self.subcategory.id)
        self.assertEqual(self.link.state, self.state_code)
        self.assertEqual(self.link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(self.link.url, 'ny.gov/link/to/statute')
        self.assertTrue(self.category.active)

    def test_init_invalid_category(self):
        with self.assertRaises(ValueError) as e:
            Link(
                subcategory_id=0,
                state=self.state_code,
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), subcategory_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            Link(
                subcategory_id=self.subcategory.id,
                state='fake-state_code',
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.link.id,
                'subcategory_id': self.subcategory.id,
                'state': self.state_code,
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
