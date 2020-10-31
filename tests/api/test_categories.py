import unittest
import json

from app import app, db
from models import Category
from tests.test_utils import clearDatabase

class CategoriesTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def tearDown(self):
    clearDatabase(db)

  def test_get_categories(self):
    category1=Category(
      title="Definition of Domestic Violence",
      active=True,
    )
    category2=Category(
      title="Worker Protections",
      active=False,
    )
    db.session.add_all([category1, category2])
    db.session.commit()

    response = self.client.get("/categories")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(len(json_response), 2)
    self.assertEqual(json_response[0], {
      "id": category1.id,
      "title": "Definition of Domestic Violence",
      "active": True
    })
    self.assertEqual(json_response[1], {
      "id": category2.id,
      "title": "Worker Protections",
      "active": False
    })

  def test_get_categories_empty(self):
    response = self.client.get("/categories")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, [])

  def test_get_category(self):
    category=Category(
      title="Definition of Domestic Violence",
      active=True,
    )
    db.session.add(category)
    db.session.commit()

    response = self.client.get("/categories/%i" % category.id)
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": category.id,
      "title": "Definition of Domestic Violence",
      "active": True
    })

  def test_get_category_doesnt_exist(self):
    response = self.client.get("/categories/1")
    self.assertEqual(response.status_code, 404)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["text"], "Category does not exist")
