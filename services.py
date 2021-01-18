from models import Category, Subcategory, Criterion, Link
from providers import post_google
import strings


def update_or_create_category(data, category=Category()):
    '''
    Takes a dict of data where the keys are fields of the category model.
    Valid keys are title, help_text, and active. The 'active' key only uses
    a False value.
    '''

    if 'title' in data.keys():
        category.title = data['title']
    if 'help_text' in data.keys():
        category.help_text = data['help_text']

    # You cannot reactivate a category after deactivating it
    if 'active' in data.keys() and not data['active']:
        category.deactivate()

    return category.save()


def update_or_create_subcategory(data, subcategory=None):
    '''
    Takes a dict of data where the keys are fields of the subcategory model.
    Valid keys are category_id, title, help_text, and active. The
    'active' key only uses a False value.

    Once created, a subcategory's category cannot be changed.
    '''
    category_id = data.get('category_id')
    if subcategory is None:
        subcategory = Subcategory(category_id=category_id)
    elif category_id is not None and category_id != subcategory.category_id:
        raise ValueError(strings.cannot_change_category)

    if 'title' in data:
        subcategory.title = data['title']
    if 'help_text' in data:
        subcategory.help_text = data['help_text']

    # You cannot reactivate a subcategory after deactivating it
    if 'active' in data and not data['active']:
        subcategory.deactivate()

    return subcategory.save()


def update_or_create_link(data, link=None):
    '''
    Takes a dict of data where the keys are fields of the link model.
    Valid keys are subcategory_id, state, text, url, and active. The 'active'
    key only uses a False value to deactivate the link.

    Once created, a link's subcategory or state cannot be changed.
    '''
    subcategory_id = data.get('subcategory_id')
    state = data.get('state')
    if link is None:
        link = Link(subcategory_id=subcategory_id, state=state)
    elif subcategory_id is not None and subcategory_id != link.subcategory_id:
        raise ValueError(strings.cannot_change_subcategory)
    elif state is not None and state != link.state:
        raise ValueError(strings.cannot_change_state)

    if 'text' in data.keys():
        link.text = data['text']
    if 'url' in data.keys():
        link.url = data['url']

    # You cannot reactivate a link after deactivating it
    if 'active' in data.keys() and not data['active']:
        link.deactivate()

    return link.save()


def update_or_create_criterion(data, criterion=None):
    '''
    Takes a dict of data where the keys are fields of the criterion model.
    Valid keys are subcategory_id, title, recommendation_text, help_text, adverse,
    and active. The 'active' key only uses a False value.

    Once created, a criterion's subcategory cannot be changed.
    '''
    subcategory_id = data.get('subcategory_id')
    if criterion is None:
        criterion = Criterion(subcategory_id=subcategory_id)
    elif subcategory_id is not None and subcategory_id != criterion.subcategory_id:
        raise ValueError(strings.cannot_change_subcategory)

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


forms = [
    'feedback',
    'report_missing_info',
    'partner_with_freefrom',
    'build_collective_survivor_power',
    'policy_ideas',
]


def submit_form_to_google(form, data):
    if form not in forms:
        raise ValueError(strings.form_not_found)
    data['form'] = form
    response = post_google(data)

    if response.get('result') == 'error':
        raise Exception

    return response
