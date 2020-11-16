import unittest
import json

from app import app, db
from models import Category, Criterion
from tests.test_utils import clearDatabase, createCategory

class CriteriaTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

    self.category=createCategory()
    db.session.add(self.category)
    db.session.commit()

  def tearDown(self):
    clearDatabase(db)

  def test_get_criteria(self):
    criterion1=Criterion(
      category_id=self.category.id,
      title="Includes economic abuse framework",
      recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
      help_text="This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
    )

    criterion2=Criterion(
      category_id=self.category.id,
      title="Uses coercive control framework",
      recommendation_text="The state's definition of domestic violence should use a framework of coercive control",
      help_text="This means that the state acknowledges the role that coercion can play in domestic violence",
    )

    criterion2.deactivate()
    db.session.add_all([criterion1, criterion2])
    db.session.commit()

    response = self.client.get("/criteria")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(len(json_response), 2)
    self.assertEqual(json_response[0], {
      "id": criterion1.id,
      "category_id": criterion1.category_id,
      "title": "Includes economic abuse framework",
      "recommendation_text": "The state's definition of domestic violence should include a framework of economic abuse",
      "help_text": "This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
      "active": True,
      "deactivated_at": None
    })

    criterion2_expected = {
      "id": criterion2.id,
      "category_id": criterion2.category_id,
      "title": "Uses coercive control framework",
      "recommendation_text": "The state's definition of domestic violence should use a framework of coercive control",
      "help_text": "This means that the state acknowledges the role that coercion can play in domestic violence",
      "active": False
    }

    # Assert that the expected results are a subset of the actual results
    self.assertTrue(criterion2_expected.items() <= json_response[1].items())
    self.assertTrue(isinstance(json_response[1]["deactivated_at"], str))

  def test_get_criteria_empty(self):
    response = self.client.get("/criteria")
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, [])

  def test_get_criterion(self):
    criterion=Criterion(
      category_id=self.category.id,
      title="Includes economic abuse framework",
      recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
      help_text="This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
    )
    db.session.add(criterion)
    db.session.commit()

    response = self.client.get("/criteria/%i" % criterion.id)
    self.assertEqual(response.status_code, 200)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response, {
      "id": criterion.id,
      "category_id": criterion.category_id,
      "title": "Includes economic abuse framework",
      "recommendation_text": "The state's definition of domestic violence should include a framework of economic abuse",
      "help_text": "This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
      "active": True,
      "deactivated_at": None
    })

  def test_get_category_doesnt_exist(self):
    response = self.client.get("/criteria/1")
    self.assertEqual(response.status_code, 404)
    json_response = json.loads(response.data.decode("utf-8"))

    self.assertEqual(json_response["text"], "Criterion does not exist")
