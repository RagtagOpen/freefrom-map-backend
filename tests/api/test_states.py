import unittest
import json

from app import app, db
from models import Category, Criterion, Link, Score
from datetime import date, datetime, timedelta
from tests.test_utils import clear_database, create_category, create_criterion, create_link

class StatesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.category1 = create_category()
        self.category2 = create_category()
        self.criterion1 = create_criterion(self.category1.id)
        self.criterion2 = create_criterion(self.category2.id)
        self.link1 = create_link(self.category1.id, 'NY')
        self.link2 = create_link(self.category2.id, 'NY')
        self.score1 = Score(
          criterion_id=self.criterion1.id,
          state='NY',
          meets_criterion=True
        )
        self.score2 = Score(
          criterion_id=self.criterion2.id,
          state='NY',
          meets_criterion=True
        )
        self.score3 = Score(
          criterion_id=self.criterion2.id,
          state='NY',
          meets_criterion=True
        )
        # score2 is more recent than score3
        self.score3.created_at = datetime.utcnow() - timedelta(5)
        self.score4 = Score(
          criterion_id=self.criterion2.id,
          state='AK',
          meets_criterion=True
        )

        Category.save_all([self.category1, self.category2])
        Criterion.save_all([self.criterion1, self.criterion2])
        Link.save_all([self.link1, self.link2])
        Score.save_all([self.score1, self.score2, self.score3, self.score4])

        self.score1_id = self.score1.id
        self.score2_id = self.score2.id


    def tearDown(self):
        clear_database(db)


    def test_get_state(self):
      response = self.client.get('/states/NY')
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


    def test_get_state_invalid_state(self):
      response = self.client.get('/states/PP')
      self.assertEqual(response.status_code, 400)


    def test_get_state_no_data(self):
      response = self.client.get('/states/KY')
      self.assertEqual(response.status_code, 200)

      json_response = json.loads(response.data.decode('utf-8'))

      self.assertIn('links', json_response)
      self.assertIn('scores', json_response)

      self.assertEqual(json_response['links'], [])
      self.assertEqual(json_response['scores'], [])
