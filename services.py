from models import (
    Category,
    Criterion,
    HonorableMention,
    InnovativePolicyIdea,
    ResourceLink
)
from providers import post_google
import strings


def update_or_create_category(data, category=Category()):
    '''
    Takes a dict of data where the keys are fields of the category model.
    Valid keys are title, help_text, and active. The
    'active' key only uses a False value.

    Once created, a category's category cannot be changed.
    '''
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
