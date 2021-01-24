import unittest

from app import app, db
from tests.test_utils import clear_database
from data.imports import import_categories


class TestImport(unittest.TestCase):
    def tearDown(self):
        clear_database(db)

    def test_import_categories(self):
      import_categories()
