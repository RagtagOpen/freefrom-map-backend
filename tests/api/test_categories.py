import unittest
import json
import datetime

from app import app, db
from models import Category
from tests.test_utils import clearDatabase, createCategory, auth_headers

class CategoriesTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def tearDown(self):
    clearDatabase(db)

  def test_get_categories(self):
    category1=Category(
      title="Definition of Domestic Violence",
      help_text="This is how a state legally defines the term 'domestic violence'",
    )
    category2=Category(
      title="Worker Protections",
      help_text="This category defines whether the state protects the jobs of victims of domestic violence",
    )
    category2.deactivate()
    db.session.add_all([category1, category2])
    db.session.commit()

    response = self.client.get("/categories")
    self.assertEqual(response.status_code, 200)

    json_response = json.loads(response.data.decode("utf-8"))
    self.assertEqual(len(json_response), 2)

    self.assertEqual(json_response[0], {
      "id": category1.id,
      "title": "Definition of Domestic Violence",
      "help_text": "This is how a state legally defines the term 'domestic violence'",
      "active": True,
      "deactivated_at": None
    })

    category_2_expected = {
      "id": category2.id,
      "title": "Worker Protections",
      "help_text": "This category defines whether the state protects the jobs of victims of domestic violence",
      "active": False,
    }

    # Assert that the expected results are a subset of the actual results
    self.assertTrue(category_2_expected.items() <= json_response[1].items())
    self.assertTrue(isinstance(json_response[1]["deactivated_at"], str))

  def test_get_categories_empty(self):
    response = self.client.get("/categories")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, [])

  def test_get_category(self):
    category=Category(
      title="Definition of Domestic Violence",
      help_text="This is how a state legally defines the term 'domestic violence'",
    )
    db.session.add(category)
    db.session.commit()

    response = self.client.get("/categories/%i" % category.id)
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": category.id,
      "title": "Definition of Domestic Violence",
      "help_text": "This is how a state legally defines the term 'domestic violence'",
      "active": True,
      "deactivated_at": None
    })

  def test_get_category_doesnt_exist(self):
    response = self.client.get("/categories/1")
    self.assertEqual(response.status_code, 404)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["text"], "Category does not exist")

  def test_post_category(self):
    data = {
      "title": "Definition of Domestic Violence",
      "help_text": "This is how a state legally defines the term 'domestic violence'"
    }

    response = self.client.post("/categories", data=data, headers=auth_headers())
    self.assertEqual(response.status_code, 201)

    new_category = Category.query.first()
    self.assertEqual(new_category.title, "Definition of Domestic Violence")
    self.assertEqual(new_category.help_text, "This is how a state legally defines the term 'domestic violence'")

    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": new_category.id,
      "title": "Definition of Domestic Violence",
      "help_text": "This is how a state legally defines the term 'domestic violence'",
      "active": True,
      "deactivated_at": None
    })

  def test_post_category_no_auth(self):
    response = self.client.post("/categories", data={}, headers={})
    self.assertEqual(response.status_code, 401)

  def test_put_category(self):
    category = createCategory()
    db.session.add(category)
    db.session.commit()

    data = {
      "title": "A New Title",
      "help_text": "Some new help text",
    }

    response = self.client.put("/categories/%i" % category.id, data=data, headers=auth_headers())
    self.assertEqual(response.status_code, 200)

    # Refresh category object
    category = Category.query.first()

    self.assertEqual(category.title, "A New Title")
    self.assertEqual(category.help_text, "Some new help text")

    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": category.id,
      "title": "A New Title",
      "help_text": "Some new help text",
      "active": True,
      "deactivated_at": None
    })

  def test_put_category_no_auth(self):
    response = self.client.put("/categories/1", data={}, headers={})
    self.assertEqual(response.status_code, 401)

  def test_put_category_deactivate(self):
    category = createCategory()
    db.session.add(category)
    db.session.commit()

    data = {
      "active": False
    }

    response = self.client.put("/categories/%i" % category.id, data=data, headers=auth_headers())
    self.assertEqual(response.status_code, 200)

    # Refresh category object
    category = Category.query.first()

    self.assertFalse(category.active)
    self.assertTrue(isinstance(category.deactivated_at, datetime.datetime))

    json_response = json.loads(response.data.decode("utf-8"))

    self.assertTrue(isinstance(json_response["deactivated_at"], str))
