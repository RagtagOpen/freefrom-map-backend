from models import Category, Criterion

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


def update_or_create_criterion(data, criterion):
  """Takes a dict of data where the keys are fields of the criterion model.
      Valid keys are category_id, title, recommendation_text, help_text, adverse,
      and active. The 'active' key only uses a False value.
  """

  if 'category_id' in data:
    criterion.category_id = data['category_id']
  if 'title' in data:
    criterion.title = data['title']
  if 'recommendation_text' in data:
    criterion.recommendation_text = data['recommendation_text']
  if 'help_text' in data:
    criterion.help_text = data['help_text']
  if 'adverse' in data:
    criterion.adverse = data['adverse']

  # You cannot reactivate a category after deactivating it
  if 'active' in data and not data['active']:
    criterion.deactivate()

  return criterion
