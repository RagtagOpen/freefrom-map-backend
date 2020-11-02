import unittest
import json
import datetime

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category, Criterion, Score
from tests.test_utils import clearDatabase, createCategory, createCriterion

class ScoreTestCase(unittest.TestCase):
  def setUp(self):
    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

    self.criterion=createCriterion(self.category.id)
    db.session.add(self.criterion)
    db.session.commit()

    self.score = Score(
      criterion_id=self.criterion.id,
      state="NY",
      meets_criterion=True
    )

    db.session.add(self.score)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_init(self):
    self.assertEqual(self.score.criterion_id, self.criterion.id)
    self.assertEqual(self.score.state, "NY")
    self.assertTrue(self.score.meets_criterion)
    self.assertTrue(isinstance(self.score.created_at, datetime.datetime))
    self.assertTrue(self.score.created_at < datetime.datetime.utcnow())
  
  def test_init_invalid_state_code(self):
    with self.assertRaises(AssertionError):
      Score(
        criterion_id=self.criterion.id,
        state="fake-state",
        meets_criterion=True
      )

  def test_serialize(self):
    self.assertDictContainsSubset(
      {
        "id": self.score.id,
        "criterion_id": self.criterion.id,
        "state": "NY",
        "meets_criterion": True
      },
      self.score.serialize()
    )

    self.assertIn("created_at", self.score.serialize().keys())
