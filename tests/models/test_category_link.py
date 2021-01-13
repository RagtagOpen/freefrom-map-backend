import unittest
import datetime
from sqlalchemy.exc import IntegrityError

from app import db
from models import CategoryLink
from strings import category_not_found, invalid_state, invalid_category_link_type
from tests.test_utils import clear_database, create_state, create_category


class CategoryLinkTestCase(unittest.TestCase):
    def setUp(self):
        self.state_code = 'AK'
        create_state(code=self.state_code)
        self.category = create_category()
        self.category_link = CategoryLink(
            category_id=self.category.id,
            state=self.state_code,
            type='innovative_policy_idea',
            text='AS 12.61.017',
            url='http://www.akleg.gov/basis/statutes.asp#12.61.017',
            description='Victims of crimes are granted protections from employer penalization if the victim is subpoenaed or requested by the prosecuting attorney to attend a court proceeding for the purpose of giving testimony, needs to report the crime to law enforcement or participates in an investigation of the offense.'
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.category_link.category_id, self.category.id)
        self.assertEqual(self.category_link.state, self.state_code)
        self.assertEqual(self.category_link.text, 'AS 12.61.017')
        self.assertEqual(self.category_link.url, 'http://www.akleg.gov/basis/statutes.asp#12.61.017')
        self.assertEqual(self.category_link.description, 'Victims of crimes are granted protections from employer penalization if the victim is subpoenaed or requested by the prosecuting attorney to attend a court proceeding for the purpose of giving testimony, needs to report the crime to law enforcement or participates in an investigation of the offense.')
        self.assertTrue(self.category_link.active)

    def test_init_invalid_category(self):
        with self.assertRaises(ValueError) as e:
            CategoryLink(
                category_id=0,
                state=self.state_code,
                type='innovative_policy_idea'
            )
        self.assertEqual(str(e.exception), category_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            CategoryLink(
                category_id=self.category.id,
                state='fake-state-code',
                type='innovative_policy_idea'
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_init_invalid_type(self):
        with self.assertRaises(ValueError) as e:
            CategoryLink(
                category_id=self.category.id,
                state='AK',
                type='random_type'
            )
        self.assertEqual(str(e.exception), invalid_category_link_type)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.category_link.id,
                'category_id': self.category.id,
                'state': self.state_code,
                'type': 'innovative_policy_idea',
                'text': 'AS 12.61.017',
                'url': 'http://www.akleg.gov/basis/statutes.asp#12.61.017',
                'description': 'Victims of crimes are granted protections from employer penalization if the victim is subpoenaed or requested by the prosecuting attorney to attend a court proceeding for the purpose of giving testimony, needs to report the crime to law enforcement or participates in an investigation of the offense.',
                'active': True,
                'deactivated_at': None,
            },
            self.category_link.serialize()
        )

    def test_deactivate(self):
        self.category_link.deactivate()

        self.assertFalse(self.category_link.active)
        self.assertTrue(isinstance(self.category_link.deactivated_at, datetime.datetime))
        self.assertTrue(self.category_link.deactivated_at < datetime.datetime.utcnow())
