import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category
from tests.test_utils import clearDatabase

class CategoryTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
    self.db = db

    self.category=Category(
        title="Definition of Domestic Violence",
        active=True,
    )

    self.db.session.add(self.category)
    self.db.session.commit()

  def tearDown(self):
    clearDatabase(self.db)

  def test_init(self):
    self.assertEqual(self.category.title, "Definition of Domestic Violence")
    self.assertTrue(self.category.active)

  def test_serialize(self):
    self.assertDictContainsSubset(
      {
        "title": "Definition of Domestic Violence",
        "active": True
      },
      self.category.serialize()
    )
