import unittest

from app import app, db
from models import State
from tests.test_utils import clear_database


class StateTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.state = State(
            code='NY',
            name='New York',
            innovative_idea='Innovative idea',
            honorable_mention='Honorable mention',
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.state.code, 'NY')
        self.assertEqual(self.state.name, 'New York')
        self.assertEqual(self.state.innovative_idea, 'Innovative idea')
        self.assertEqual(self.state.honorable_mention, 'Honorable mention')

    def test_serialize(self):
        self.assertEqual(
            {
                'code': 'NY',
                'name': 'New York',
                'innovative_idea': 'Innovative idea',
                'honorable_mention': 'Honorable mention',
            },
            self.state.serialize()
        )
