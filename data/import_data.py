import yaml
import os

from app import db  # noqa: F401
from models import (
    Category,
    Criterion,
    HonorableMention,
    InnovativePolicyIdea,
    Score,
    State,
    StateGrade,
    StateCategoryGrade,
    ResourceLink
)
from tests.test_utils import clear_database

SCRIPT_DIR = os.path.dirname(__file__)


def import_data():
    print('Clearing database')
    clear_database(db)

    print('Importing categories')
    import_categories()

    for filename in os.listdir(absolute_file_path('states')):
        state = filename.split('.yaml')[0]
        print(f'Importing state: {state}')

        import_state(absolute_file_path(f'states/{filename}'))


def absolute_file_path(file_name):
    return os.path.join(SCRIPT_DIR, file_name)


def import_state(path):
    with open(path) as file:
        state_data = yaml.load(file, Loader=yaml.FullLoader)
        code = state_data['code']
        name = state_data['name']

        State(code=code, name=name).save()

        grade = state_data['grade']
        StateGrade(state_code=code, grade=grade).save()

        categories_data = state_data['categories']

        for category_data in categories_data:
            category = Category.query.filter_by(title=category_data['title']).first()

            StateCategoryGrade(
                state_code=code,
                category_id=category.id,
                grade=category_data['grade']
            ).save()

            innovative_policy_idea = category_data['innovative_policy_idea']
            if innovative_policy_idea:
                InnovativePolicyIdea(
                    category_id=category.id,
                    state=code,
                    text=innovative_policy_idea['text'],
                    url=innovative_policy_idea['url'],
                    description=innovative_policy_idea['description'],
                ).save()

            honorable_mention = category_data['honorable_mention']
            if honorable_mention:
                HonorableMention(
                    category_id=category.id,
                    state=code,
                    text=honorable_mention['text'],
                    url=honorable_mention['url'],
                    description=honorable_mention['description'],
                ).save()

            resource_links = []
            for resource_link in category_data['resource_links']:
                resource_links.append(
                    ResourceLink(
                        category_id=category.id,
                        state=code,
                        text=resource_link['text'],
                        url=resource_link['url']
                    )
                )

            ResourceLink.save_all(resource_links)

            scores = []
            for criterion in Criterion.query.filter_by(category_id=category.id).all():
                meets_criterion = criterion.id in category_data['criteria_met']

                scores.append(
                    Score(
                        state=code,
                        criterion_id=criterion.id,
                        meets_criterion=meets_criterion
                    )
                )

            Score.save_all(scores)


def import_categories():
    full_path = absolute_file_path('categories.yml')

    with open(full_path) as file:
        categories_data = yaml.load(file, Loader=yaml.FullLoader)
        for category_data in categories_data:
            category = Category(title=category_data['title'],
                                help_text=category_data['help_text']).save()

            criteria = []
            for criterion_data in category_data['ideal_criteria']:
                criteria.append(
                    Criterion(id=criterion_data['id'],
                              category_id=category.id, title=criterion_data['text'])
                )

            for criterion_data in category_data['adverse_criteria']:
                criteria.append(
                    Criterion(id=criterion_data['id'], category_id=category.id,
                              title=criterion_data['text'], adverse=True)
                )

            Criterion.save_all(criteria)
