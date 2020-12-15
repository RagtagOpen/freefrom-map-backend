import unittest
import json
import datetime

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Category, Link
from tests.test_utils import clearDatabase, createCategory

class LinkTestCase(unittest.TestCase):
  def setUp(self):
    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

    self.link = Link(
      category_id=self.category.id,
      state="NY",
      text="Section 20 of Statute 39-B",
      url="ny.gov/link/to/statute"
    )

    db.session.add(self.link)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_init(self):
    self.assertEqual(self.link.category_id, self.category.id)
    self.assertEqual(self.link.state, "NY")
    self.assertEqual(self.link.text, "Section 20 of Statute 39-B")
    self.assertEqual(self.link.url, "ny.gov/link/to/statute")
    self.assertTrue(self.category.active)

  def test_init_invalid_state_code(self):
    with self.assertRaises(AssertionError):
      Link(
        category_id=self.category.id,
        state="fake-state",
        text="Section 20 of Statute 39-B",
        url="ny.gov/link/to/statute"
      )

  def test_serialize(self):
    self.assertEqual(
      {
        "id": self.link.id,
        "category_id": self.category.id,
        "state": "NY",
        "text": "Section 20 of Statute 39-B",
        "url": "ny.gov/link/to/statute",
        "active": True,
        "deactivated_at": None
      },
      self.link.serialize()
    )

  def test_deactivate(self):
    self.link.deactivate()

    self.assertFalse(self.link.active)
    self.assertTrue(isinstance(self.link.deactivated_at, datetime.datetime))
    self.assertTrue(self.link.deactivated_at < datetime.datetime.utcnow())