import json
import os
import requests
import unittest

import models
from auth import AUTH0_DOMAIN, API_AUDIENCE

def clearDatabase(db):
  db.session.query(models.Link).delete()
  db.session.query(models.Score).delete()
  db.session.query(models.Criterion).delete()
  db.session.query(models.Category).delete()
  db.session.commit()

def createCategory():
  return models.Category(
    title="Definition of Domestic Violence",
    help_text="This is how a state legally defines the term 'domestic violence'",
  )

def createCriterion(category_id):
  return models.Criterion(
    category_id=category_id,
    title="Includes economic abuse framework",
    recommendation_text="The state's definition of domestic violence should include a framework of economic abuse",
    help_text="This means that the state acknowledges the role that economic control and abuse can play in domestic violence",
    adverse=False
  )

def require_auth0_secrets():
  return unittest.skipIf(
    not os.environ.get("AUTH0_CLIENT_ID") or not os.environ.get("AUTH0_CLIENT_SECRET"),
    "Cannot run test without AUTH0_CLIENT_ID and AUTH0_CLIENT_SECRET environment variables"
  )

def auth_headers():
  data = {
    "client_id": os.environ.get('AUTH0_CLIENT_ID'),
    "client_secret": os.environ.get('AUTH0_CLIENT_SECRET'),
    "audience": API_AUDIENCE,
    "grant_type":"client_credentials"
  }

  jwt_response = requests.post(f'https://{AUTH0_DOMAIN}/oauth/token', data=data)
  jwt = json.loads(jwt_response.text)['access_token']

  return {'Authorization': f'Bearer {jwt}'}
