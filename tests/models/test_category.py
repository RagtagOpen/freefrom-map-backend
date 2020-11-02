import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category
from tests.test_utils import clearDatabase

class CategoryTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

    self.category=Category(
        title="Definition of Domestic Violence",
        help_text="This is how a state legally defines the term 'domestic violence'",
        active=True,
    )

    db.session.add(self.category)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_init(self):
    self.assertEqual(self.category.title, "Definition of Domestic Violence")
    self.assertEqual(self.category.help_text, "This is how a state legally defines the term 'domestic violence'")
    self.assertTrue(self.category.active)

  def test_serialize(self):
    self.assertEqual(
      {
        "id": self.category.id,
        "title": "Definition of Domestic Violence",
        "help_text": "This is how a state legally defines the term 'domestic violence'",
        "active": True
      },
      self.category.serialize()
    )
