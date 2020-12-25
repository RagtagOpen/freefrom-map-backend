from models import Category, Criterion, Link
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
    elif subcategory_id and subcategory_id != link.subcategory_id:
        raise ValueError(strings.cannot_change_subcategory)
    elif state and state != link.state:
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
    elif subcategory_id and subcategory_id != criterion.subcategory_id:
        raise ValueError(strings.cannot_change_subcategory)

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

    return criterion.save()
