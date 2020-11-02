import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category, Criterion, Link
from tests.test_utils import clearDatabase

class LinkTestCase(unittest.TestCase):
  def setUp(self):
    self.category=Category(
        title="Definition of Domestic Violence",
        active=True,
    )

    db.session.add(self.category)
    db.session.commit()

    self.criterion=Criterion(
      category_id=self.category.id,
      title="Includes economic abuse framework",
      recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
      active=True
    )

    db.session.add(self.criterion)
    db.session.commit()

    self.link = Link(
      criterion_id=self.criterion.id,
      state="NY",
      text="Section 20 of Statute 39-B",
      url="ny.gov/link/to/statute"
    )

    db.session.add(self.link)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_init(self):
    self.assertEqual(self.link.criterion_id, self.criterion.id)
    self.assertEqual(self.link.state, "NY")
    self.assertTrue(self.link.text)
    self.assertTrue(self.link.url)
  
  def test_init_invalid_state_code(self):
    with self.assertRaises(AssertionError):
      Link(
        criterion_id=self.criterion.id,
        state="fake-state",
        text="Section 20 of Statute 39-B",
        url="ny.gov/link/to/statute"
      )

  def test_serialize(self):
    self.assertEqual(
      {
        "id": self.link.id,
        "criterion_id": self.criterion.id,
        "state": "NY",
        "text": "Section 20 of Statute 39-B",
        "url": "ny.gov/link/to/statute"
      },
      self.link.serialize()
    )
