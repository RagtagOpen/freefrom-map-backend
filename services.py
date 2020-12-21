from models import Category, Criterion, Link


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
    Valid keys are category_id, state, text, url, and active. The 'active'
    key only uses a False value to deactivate the link.
    '''

    if link is None:
        # TODO: Raise an appropriate error if category_id and state are not present
        #  (see issue #57)
        link = Link(category_id=data['category_id'], state=data['state'])

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
    '''

    if criterion is None:
        # TODO: Raise an appropriate error if category_id and state are not present
        #  (see issue #57)
        criterion = Criterion(category_id=data['category_id'])

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

def state_information(state):
    links = Link.query.filter_by(state=state, active=True)

    subquery = Score.query(
        Score.category,
        func.max(Score.created_at).label('most_recent')
    ).filter_by(state=state_).group_by(Score.state, Score.category).subquery

    scores = Score.query.join(
        subquery,
        and_(
            Score.category_id == subquery.c.category_id,
            Score.created_at == subquery.c.most_recent
        )
    )

    return {
        'links': links,
        'scores': scores
    }
