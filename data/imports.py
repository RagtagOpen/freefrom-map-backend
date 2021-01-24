import yaml
import os

SCRIPT_DIR = os.path.dirname(__file__)

def absolute_file_path(file_name):
  return os.path.join(SCRIPT_DIR, file_name)


def import_categories():
  full_path = absolute_file_path('categories.yml')
  with open(full_path) as file:
    categories_info = yaml.load(file, Loader=yaml.FullLoader)
