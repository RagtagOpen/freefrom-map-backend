import unittest
import json

from app import app, db
from models import Category, Criterion, Link
from tests.test_utils import clearDatabase, createCategory, createCriterion

class LinksTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

    self.criterion=createCriterion(self.category.id)
    db.session.add(self.criterion)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_get_links(self):
    link1=Link(
      criterion_id=self.criterion.id,
      state="NY",
      text="Section 20 of Statute 39-B",
      url="ny.gov/link/to/statute",
    )

    link2=Link(
      criterion_id=self.criterion.id,
      state="AZ",
      text="Statute 20 of Policy ABC",
      url="az.gov/link/to/statute",
    )

    db.session.add_all([link1, link2])
    db.session.commit()

    response = self.client.get("/links")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(len(json_response), 2)
    self.assertEqual(json_response[0], {
      "id": link1.id,
      "criterion_id": link1.criterion_id,
      "state": "NY",
      "text": "Section 20 of Statute 39-B",
      "url": "ny.gov/link/to/statute",
    })
    self.assertEqual(json_response[1], {
      "id": link2.id,
      "criterion_id": link2.criterion_id,
      "state": "AZ",
      "text": "Statute 20 of Policy ABC",
      "url": "az.gov/link/to/statute",
    })

  def test_get_links_empty(self):
    response = self.client.get("/links")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, [])

  def test_get_link(self):
    link=Link(
      criterion_id=self.criterion.id,
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
      "criterion_id": link.criterion_id,
      "state": "NY",
      "text": "Section 20 of Statute 39-B",
      "url": "ny.gov/link/to/statute",
    })

  def test_get_link_doesnt_exist(self):
    response = self.client.get("/links/1")
    self.assertEqual(response.status_code, 404)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["text"], "Link does not exist")
