import unittest
import json
import datetime

from app import app, db
from models import Category, Link
from tests.test_utils import clear_database, create_category, auth_headers

class StatesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.category1 = create_category()
        self.category2 = create_category()
        self.criterion1 = create_criterion(self.category1.id)
        self.criterion2 = create_criterion(self.category2.id)
        self.link1 = create_link(self.category1.id)
        self.link2 = create_link(self.category2.id)

        db.session.add(self.category)
        db.session.commit()

    def tearDown(self):
        clear_database(db)
