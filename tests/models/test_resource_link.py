import unittest
import datetime

from app import db
from models import ResourceLink
from strings import subcategory_not_found, invalid_state
from tests.test_utils import clear_database, create_state, create_category, create_subcategory


class ResourceLinkTestCase(unittest.TestCase):
    def setUp(self):
        self.state_code = 'NY'
        create_state(code=self.state_code)
        self.category = create_category()
        self.subcategory = create_subcategory(self.category.id)
        self.resource_link = ResourceLink(
            subcategory_id=self.subcategory.id,
            state=self.state_code,
            text='Section 20 of Statute 39-B',
            url='ny.gov/link/to/statute',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.resource_link.subcategory_id, self.subcategory.id)
        self.assertEqual(self.resource_link.state, self.state_code)
        self.assertEqual(self.resource_link.text, 'Section 20 of Statute 39-B')
        self.assertEqual(self.resource_link.url, 'ny.gov/link/to/statute')
        self.assertEqual(self.resource_link.type, 'resource_link')
        self.assertTrue(self.category.active)

    def test_init_invalid_category(self):
        with self.assertRaises(ValueError) as e:
            ResourceLink(
                subcategory_id=0,
                state=self.state_code,
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), subcategory_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            ResourceLink(
                subcategory_id=self.subcategory.id,
                state='fake-state-code',
                text='Section 20 of Statute 39-B',
                url='ny.gov/link/to/statute',
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.resource_link.id,
                'subcategory_id': self.subcategory.id,
                'state': self.state_code,
                'text': 'Section 20 of Statute 39-B',
                'url': 'ny.gov/link/to/statute',
                'active': True,
                'deactivated_at': None,
            },
            self.resource_link.serialize()
        )

    def test_deactivate(self):
        self.resource_link.deactivate()

        self.assertFalse(self.resource_link.active)
        self.assertTrue(isinstance(self.resource_link.deactivated_at, datetime.datetime))
        self.assertTrue(self.resource_link.deactivated_at < datetime.datetime.utcnow())
