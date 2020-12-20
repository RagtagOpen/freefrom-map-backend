import unittest
import datetime

from app import app, db
from models import Criterion
from tests.test_utils import clear_database, create_category


class CriterionTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.category = create_category()
        db.session.add(self.category)
        db.session.commit()

        self.criterion = Criterion(
            category_id=self.category.id,
            title='Includes economic abuse framework',
            recommendation_text=(
                "The state's definition of domestic violence should include a framework of "
                'economic abuse'
            ),
            help_text=(
                'This means that the state acknowledges the role that economic control and abuse '
                'can play in domestic violence'
            ),
            adverse=False,
        )

        db.session.add(self.criterion)
        db.session.commit()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.criterion.category_id, self.category.id)
        self.assertEqual(self.criterion.title, 'Includes economic abuse framework')
        self.assertEqual(
            self.criterion.recommendation_text,
            "The state's definition of domestic violence should include a framework of economic "
            'abuse',
        )
        self.assertEqual(
            self.criterion.help_text,
            'This means that the state acknowledges the role that economic control and abuse can '
            'play in domestic violence',
        ),
        self.assertTrue(self.criterion.active)
        self.assertFalse(self.criterion.adverse)

    def test_serialize(self):
        self.assertEqual(
            {
                'id': self.criterion.id,
                'category_id': self.category.id,
                'title': 'Includes economic abuse framework',
                'recommendation_text':
                    "The state's definition of domestic violence should include a framework of "
                    'economic abuse',
                'help_text':
                    'This means that the state acknowledges the role that economic control and '
                    'abuse can play in domestic violence',
                'active': True,
                'deactivated_at': None,
                'adverse': False,
            },
            self.criterion.serialize()
        )

    def test_deactivate(self):
        self.criterion.deactivate()

        self.assertFalse(self.criterion.active)
        self.assertTrue(isinstance(self.criterion.deactivated_at, datetime.datetime))
        self.assertTrue(self.criterion.deactivated_at < datetime.datetime.utcnow())
