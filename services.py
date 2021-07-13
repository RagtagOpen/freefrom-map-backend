from models import (
    Category,
    Criterion,
    StateGrade,
    StateCategoryGrade,
    Score,
    HonorableMention,
    InnovativePolicyIdea,
    ResourceLink
)
from providers import post_google
import strings


def update_or_create_category(data, category=None):
    '''
    Takes a dict of data where the keys are fields of the category model.
    Valid keys are title, help_text, and active. The
    'active' key only uses a False value.

    Once created, a category's category cannot be changed.
    '''

    if category is None:
        if 'id' in data:
            category = Category(id=data.get('id'))
        else:
            category = Category()

    if 'title' in data:
        category.title = data['title']
    if 'help_text' in data:
        category.help_text = data['help_text']

    # You cannot reactivate a category after deactivating it
    if 'active' in data and not data['active']:
        category.deactivate()

    return category.save()


def get_subclass_from_link_type(link_type: str):
    subclasses_by_type = {
        strings.resource_link: ResourceLink,
        strings.honorable_mention: HonorableMention,
        strings.innovative_policy_idea: InnovativePolicyIdea,
    }

    subclass = subclasses_by_type.get(link_type)

    if link_type is not None and subclass is None:
        raise ValueError(strings.invalid_link_type)

    return subclass


def update_or_create_link(data, link=None):
    '''
    Takes a dict of data where the keys are fields of the link model.
    Valid keys are category_id, state, text, url, and active. The 'active'
    key only uses a False value to deactivate the link.

    Once created, a link's category or state cannot be changed.
    '''
    category_id = data.get('category_id')
    state = data.get('state')
    link_type = data.get('type')
    subclass = get_subclass_from_link_type(link_type)

    if link is None:
        if subclass is None:
            raise ValueError(strings.require_link_type)

        if 'id' in data:
            link = subclass(category_id=category_id, state=state, id=data.get('id'))
        else:
            link = subclass(category_id=category_id, state=state)
    elif category_id is not None and category_id != link.category_id:
        raise ValueError(strings.cannot_change_category)
    elif state is not None and state != link.state:
        raise ValueError(strings.cannot_change_state)
    elif link_type is not None and not isinstance(link, subclass):
        raise ValueError(strings.cannot_change_type)

    if 'text' in data.keys():
        link.text = data['text']
    if 'url' in data.keys():
        link.url = data['url']
    if 'description' in data.keys():
        link.description = data['description']

    # You cannot reactivate a link after deactivating it
    if 'active' in data.keys() and not data['active']:
        link.deactivate()

    return link.save()


def update_or_create_criterion(data, criterion=None):
    '''
    Takes a dict of data where the keys are fields of the criterion model.
    Valid keys are category_id, title, recommendation_text, help_text, adverse,
    and active. The 'active' key only uses a False value.

    Once created, a criterion's category cannot be changed.
    '''
    category_id = data.get('category_id')

    if criterion is None:
        if 'id' in data:
            criterion = Criterion(id=data.get('id'), category_id=category_id)
        else:
            criterion = Criterion(category_id=category_id)

    elif category_id is not None and category_id != criterion.category_id:
        raise ValueError(strings.cannot_change_category)

    if 'title' in data:
        criterion.title = data['title']
    if 'recommendation_text' in data:
        criterion.recommendation_text = data['recommendation_text']
    if 'help_text' in data:
        criterion.help_text = data['help_text']
    if 'adverse' in data:
        criterion.adverse = data['adverse']

    # You cannot reactivate a criterion after deactivating it
    if 'active' in data and not data['active']:
        criterion.deactivate()

    return criterion.save()


def update_or_create_score(criterion_id, state_code, meets_criterion):
    '''
    Takes a criterion id, a state code, and whether the state meets that criterion.
    If the current score for this state/criterion does not match what is provided,
    or no score exists, a new score is created with this information.
    '''
    score = Score.query.filter_by(criterion_id=criterion_id, state=state_code) \
        .order_by(Score.created_at.desc()).first()

    if score is None or score.meets_criterion != meets_criterion:
        score = Score(
            criterion_id=criterion_id,
            state=state_code,
            meets_criterion=meets_criterion,
        ).save()

    return score


def update_or_create_state_category_grade(category_id, state_code, grade):
    '''
    Takes a category id, a state code, and the grade for that state and category.
    If the current grade for this state/category does not match what is provided, or if no grade
    exists, a new grade is created with this information.
    '''
    state_category_grade = StateCategoryGrade.query.filter_by(
        state_code=state_code,
        category_id=category_id,
    ).order_by(StateCategoryGrade.created_at.desc()).first()

    if state_category_grade is None or state_category_grade.grade != grade:
        state_category_grade = StateCategoryGrade(
            state_code=state_code,
            category_id=category_id,
            grade=grade,
        ).save()

    return state_category_grade


def update_state(data, state):
    '''
    Updates information about the provided state, including the total, quote, overall grade,
    scores, category grades, and links. It is not possible to create a new state.
    '''
    if 'total' in data:
        state.total = data['total']
    if 'quote' in data:
        state.quote = data['quote']
    if 'grade' in data and int(data['grade']) != state.grades[0].grade:
        StateGrade(
            state_code=state.code,
            grade=int(data['grade'])
        ).save()
    if 'criteria_met' in data:
        for criterion_met in data['criteria_met']:
            update_or_create_score(
                criterion_met['id'],
                state.code,
                criterion_met['meets_criterion'],
            )
    if 'category_grades' in data:
        for category_grade_data in data['category_grades']:
            update_or_create_state_category_grade(
                category_grade_data['id'],
                state.code,
                int(category_grade_data['grade']),
            )
    for link_type in ['resource_link', 'honorable_mention', 'innovative_policy_idea']:
        for link_data in data[f'{link_type}s']:
            link = get_subclass_from_link_type(link_type).query.get(link_data['id'])
            link_data['type'] = link_type

            update_or_create_link(link_data, link)

    return state.save()


forms = [
    'give-feedback',
    'report-missing-info',
    'partner-with-freefrom',
    'survivor-power',
    'policy-ideas',
]


def submit_form_to_google(form, data):
    if form not in forms:
        raise ValueError(strings.form_not_found)
    data['form'] = form
    response = post_google(data)

    if response.get('result') == 'error':
        raise Exception

    return response
