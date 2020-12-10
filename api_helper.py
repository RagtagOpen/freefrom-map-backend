from models import Category

def build_category(data, category=Category()):
  if 'title' in data.keys():
    category.title = data['title']
  if 'help_text' in data.keys():
    category.help_text = data['help_text']
  if 'active' in data.keys() and data['active'] == 'False':
    # You cannot reactivate a category after deactivating it
    category.deactivate()

  return category
