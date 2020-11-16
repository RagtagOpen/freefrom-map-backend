import unittest
import json
import datetime

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category, Criterion
from tests.test_utils import clearDatabase, createCategory

class CriterionTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

    self.criterion=Criterion(
      category_id=self.category.id,
      title="Includes economic abuse framework",
      recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
      help_text="This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
    )

    db.session.add(self.criterion)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_init(self):
    self.assertEqual(self.criterion.category_id, self.category.id)
    self.assertEqual(self.criterion.title, "Includes economic abuse framework")
    self.assertEqual(self.criterion.recommendation_text, "The state's definition of domestic violence should include a framework of economic abuse")
    self.assertEqual(self.criterion.help_text, "This means that the state acknowledges the role that economic control and abuse can play in domestic violence")
    self.assertTrue(self.criterion.active)

  def test_serialize(self):
    self.assertEqual(
      {
        "id": self.criterion.id,
        "category_id": self.category.id,
        "title": "Includes economic abuse framework",
        "recommendation_text": "The state's definition of domestic violence should include a framework of economic abuse",
        "help_text": "This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
        "active": True,
        "deactivated_at": None
      },
      self.criterion.serialize()
    )

  def test_deactivate(self):
    self.criterion.deactivate()

    self.assertFalse(self.criterion.active)
    self.assertTrue(isinstance(self.criterion.deactivated_at, datetime.datetime))
    self.assertTrue(self.criterion.deactivated_at < datetime.datetime.utcnow())