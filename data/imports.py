import yaml
import os

from models import Category, Subcategory, Criterion

SCRIPT_DIR = os.path.dirname(__file__)


def absolute_file_path(file_name):
    return os.path.join(SCRIPT_DIR, file_name)


def import_categories():
    full_path = absolute_file_path('categories.yml')
    with open(full_path) as file:
        categories_data = yaml.load(file, Loader=yaml.FullLoader)
        for category_data in categories_data:
            category = Category(title=category_data['title']).save()

            for subcategory_data in category_data['subcategories']:
                subcategory = Subcategory(
                    category_id=category.id,
                    title=subcategory_data['title']
                ).save()

                criteria = []
                for criterion_data in subcategory_data['ideal_criteria']:
                    criteria.append(
                        Criterion(subcategory_id=subcategory.id, title=criterion_data)
                    )

                for criterion_data in subcategory_data['adverse_criteria']:
                    criteria.append(
                        Criterion(subcategory_id=subcategory.id,
                                  title=criterion_data, adverse=True)
                    )

                Criterion.save_all(criteria)
