import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category, Criterion
from tests.test_utils import clearDatabase

class CriterionTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
    self.db = db

    self.category=Category(
        title="Definition of Domestic Violence",
        active=True,
    )
    self.db.session.add(self.category)
    self.db.session.commit()

    self.criterion=Criterion(
      category_id=self.category.id,
      title="Includes economic abuse framework",
      recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
      active=True
    )

    self.db.session.add(self.criterion)
    self.db.session.commit()

  def tearDown(self):
    clearDatabase(self.db)

  def test_init(self):
    self.assertEqual(self.criterion.category_id, self.category.id)
    self.assertEqual(self.criterion.title, "Includes economic abuse framework")
    self.assertEqual(self.criterion.recommendation_text, "The state's definition of domestic violence should include a framework of economic abuse")
    self.assertTrue(self.criterion.active)

  def test_serialize(self):
    self.assertDictContainsSubset(
      {
        "category_id": self.category.id,
        "title": "Includes economic abuse framework",
        "recommendation_text": "The state's definition of domestic violence should include a framework of economic abuse",
        "active": True
      },
      self.criterion.serialize()
    )
