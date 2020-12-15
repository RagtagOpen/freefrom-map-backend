from models import Category

def update_or_create_category(data, category=Category()):
  """Takes a dict of data where the keys are fields of the category model.
      Valid keys are title, help_text, and active. The 'active' key only uses
      a False value.
  """

  if 'title' in data.keys():
    category.title = data['title']
  if 'help_text' in data.keys():
    category.help_text = data['help_text']

  # You cannot reactivate a category after deactivating it
  if 'active' in data.keys() and data['active'] == 'False':
    category.deactivate()

  return category
