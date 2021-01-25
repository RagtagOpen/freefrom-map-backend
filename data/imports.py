import yaml
import os

from models import (
    Category,
    Criterion,
    HonorableMention,
    InnovativePolicyIdea,
    Score,
    State,
    StateGrade,
    StateSubcategoryGrade,
    Subcategory,
    ResourceLink
)

SCRIPT_DIR = os.path.dirname(__file__)


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

        subcategories_data = state_data['subcategories']

        for subcategory_data in subcategories_data:
            subcategory = Subcategory.query.filter_by(title=subcategory_data['title']).first()

            StateSubcategoryGrade(
                state_code=code,
                subcategory_id=subcategory.id,
                grade=subcategory_data['grade']
            ).save()

            innovative_policy_idea = subcategory_data['innovative_policy_idea']
            if innovative_policy_idea:
                InnovativePolicyIdea(
                    subcategory_id=subcategory.id,
                    state=code,
                    text=innovative_policy_idea['text'],
                    url=innovative_policy_idea['url'],
                    description=innovative_policy_idea['description'],
                ).save()

            honorable_mention = subcategory_data['honorable_mention']
            if honorable_mention:
                HonorableMention(
                    subcategory_id=subcategory.id,
                    state=code,
                    text=honorable_mention['text'],
                    url=honorable_mention['url'],
                    description=honorable_mention['description'],
                ).save()

            resource_links = []
            for resource_link in subcategory_data['resource_links']:
                resource_links.append(
                    ResourceLink(
                        subcategory_id=subcategory.id,
                        state=code,
                        text=resource_link['text'],
                        url=resource_link['url']
                    )
                )

            ResourceLink.save_all(resource_links)

            scores = []
            for criterion in Criterion.query.filter_by(subcategory_id=subcategory.id).all():
                meets_criterion = criterion.title in subcategory_data['criteria_met']

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
