from models import Category, Link

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

def update_or_create_link(data, link=None):
  """Takes a dict of data where the keys are fields of the link model.
     Valid keys are category_id, state, text, url, and active. The 'active'
     key only uses a False value to deactivate the link.
  """

  if link is None:
    # TODO: Raise an appropriate error if category_id and state are not present
    #  (see issue #57)
    link = Link(category_id=data["category_id"], state=data["state"])

  if 'text' in data.keys():
    link.text = data['text']
  if 'url' in data.keys():
    link.url = data['url']

  # You cannot reactivate a link after deactivating it
  if 'active' in data.keys() and data['active'] == 'False':
    link.deactivate()

  return link
