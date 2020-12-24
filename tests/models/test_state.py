import unittest
import datetime

from app import app, db
from models import State
from tests.test_utils import clear_database, create_criterion


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.state = State(
            code='NY',
            name="New York",
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.state.code, 'NY')
        self.assertEqual(self.state.name, 'New York')

    def test_serialize(self):
        self.assertEqual(
            {
                'code': 'NY',
                'name': 'New York',
            },
            self.state.serialize()
        )
