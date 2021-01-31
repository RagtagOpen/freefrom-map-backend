import unittest
import datetime

from app import db
from models import HonorableMention
from strings import category_not_found, invalid_state
from tests.test_utils import clear_database, create_state, create_category


class HonorableMentionTestCase(unittest.TestCase):
    def setUp(self):
        self.state_code = 'AK'
        create_state(code=self.state_code)
        self.category = create_category()
        self.honorable_mention = HonorableMention(
            category_id=self.category.id,
            state=self.state_code,
            text='AS 12.61.017',
            url='http://www.akleg.gov/basis/statutes.asp#12.61.017',
            description='Victims of crimes are granted protections from employer...'
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.honorable_mention.category_id, self.category.id)
        self.assertEqual(self.honorable_mention.state, self.state_code)
        self.assertEqual(self.honorable_mention.text, 'AS 12.61.017')
        self.assertEqual(
            self.honorable_mention.url,
            'http://www.akleg.gov/basis/statutes.asp#12.61.017'
        )
        self.assertEqual(
            self.honorable_mention.description,
            'Victims of crimes are granted protections from employer...'
        )
        self.assertTrue(self.honorable_mention.active)

    def test_init_invalid_category(self):
        with self.assertRaises(ValueError) as e:
            HonorableMention(
                category_id=0,
                state=self.state_code,
            )
        self.assertEqual(str(e.exception), category_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            HonorableMention(
                category_id=self.category.id,
                state='fake-state-code',
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.honorable_mention.id,
                'category_id': self.category.id,
                'state': self.state_code,
                'text': 'AS 12.61.017',
                'url': 'http://www.akleg.gov/basis/statutes.asp#12.61.017',
                'description': 'Victims of crimes are granted protections from employer...',
                'active': True,
                'deactivated_at': None,
            },
            self.honorable_mention.serialize()
        )

    def test_deactivate(self):
        self.honorable_mention.deactivate()

        self.assertFalse(self.honorable_mention.active)
        self.assertTrue(isinstance(self.honorable_mention.deactivated_at, datetime.datetime))
        self.assertTrue(self.honorable_mention.deactivated_at < datetime.datetime.utcnow())
