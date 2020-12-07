import unittest
import json

from app import app, db
from models import Category, Link
from tests.test_utils import clearDatabase, createCategory

class LinksTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_get_links(self):
    link1=Link(
      category_id=self.category.id,
      state="NY",
      text="Section 20 of Statute 39-B",
      url="ny.gov/link/to/statute",
    )

    link2=Link(
      category_id=self.category.id,
      state="AZ",
      text="Statute 20 of Policy ABC",
      url="az.gov/link/to/statute",
    )

    link2.deactivate()

    db.session.add_all([link1, link2])
    db.session.commit()

    response = self.client.get("/links")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(len(json_response), 2)
    self.assertEqual(json_response[0], {
      "id": link1.id,
      "category_id": link1.category_id,
      "state": "NY",
      "text": "Section 20 of Statute 39-B",
      "url": "ny.gov/link/to/statute",
      "active": True,
      "deactivated_at": None
    })

    link2_expected = {
      "id": link2.id,
      "category_id": link2.category_id,
      "state": "AZ",
      "text": "Statute 20 of Policy ABC",
      "url": "az.gov/link/to/statute",
      "active": False
    }

    # Assert that the expected results are a subset of the actual results
    self.assertTrue(link2_expected.items() <= json_response[1].items())
    self.assertTrue(isinstance(json_response[1]["deactivated_at"], str))

  def test_get_links_empty(self):
    response = self.client.get("/links")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, [])

  def test_get_link(self):
    link=Link(
      category_id=self.category.id,
      state="NY",
      text="Section 20 of Statute 39-B",
      url="ny.gov/link/to/statute",
    )
    db.session.add(link)
    db.session.commit()

    response = self.client.get("/links/%i" % link.id)
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": link.id,
      "category_id": link.category_id,
      "state": "NY",
      "text": "Section 20 of Statute 39-B",
      "url": "ny.gov/link/to/statute",
      "active": True,
      "deactivated_at": None
    })

  def test_get_link_doesnt_exist(self):
    response = self.client.get("/links/1")
    self.assertEqual(response.status_code, 404)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["text"], "Link does not exist")
