import unittest
import json

from app import app, db
from models import Score
from datetime import datetime, timedelta
from tests.test_utils import clear_database, create_state, create_category, create_criterion, create_link


class StatesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.state1 = 'NY'
        self.state2 = 'AK'
        create_state(code=self.state1)
        create_state(code=self.state2)

        self.category1 = create_category()
        self.category2 = create_category()
        self.criterion1 = create_criterion(self.category1.id)
        self.criterion2 = create_criterion(self.category2.id)
        self.link1 = create_link(self.category1.id, self.state1)
        self.link2 = create_link(self.category2.id, self.state1)
        self.score1 = Score(
            criterion_id=self.criterion1.id,
            state=self.state1,
            meets_criterion=True,
        )
        self.score2 = Score(
            criterion_id=self.criterion2.id,
            state=self.state1,
            meets_criterion=False,
        )
        self.score3 = Score(
            criterion_id=self.criterion2.id,
            state=self.state1,
            meets_criterion=True,
        )
        # score2 is more recent than score3
        self.score3.created_at = datetime.utcnow() - timedelta(5)
        self.score4 = Score(
            criterion_id=self.criterion2.id,
            state=self.state2,
            meets_criterion=True,
        )

        Score.save_all([self.score1, self.score2, self.score3, self.score4])

        self.score1_id = self.score1.id
        self.score2_id = self.score2.id

    def tearDown(self):
        clear_database(db)

    def test_get_state(self):
        response = self.client.get(f'/states/{self.state1}')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertIn('links', json_response)
        self.assertIn('scores', json_response)

        links = json_response['links']
        scores = json_response['scores']

        score1 = Score.query.get(self.score1_id)
        score2 = Score.query.get(self.score2_id)

        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], self.link1.serialize())
        self.assertEqual(links[1], self.link2.serialize())

        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[0], score1.serialize())
        self.assertEqual(scores[1], score2.serialize())
        self.assertTrue(scores[0]['meets_criterion'])
        self.assertFalse(scores[1]['meets_criterion'])

    def test_get_state_doesnt_exist(self):
        response = self.client.get('/states/PP')
        self.assertEqual(response.status_code, 400)

    def test_get_state_no_data(self):
        state = create_state(code='KY')
        response = self.client.get('/states/KY')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertIn('links', json_response)
        self.assertIn('scores', json_response)

        self.assertEqual(json_response['links'], [])
        self.assertEqual(json_response['scores'], [])
