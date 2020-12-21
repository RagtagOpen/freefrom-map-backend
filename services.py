from models import Category, Criterion, Link, Score
from app import db
from sqlalchemy import func, and_


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
    links = Link.query.filter_by(state=state, active=True).all()

    # https://stackoverflow.com/questions/58333162/how-to-get-top-n-results-per-group-from-a-pool-of-ids-in-sqlalchemy
    subquery = db.session.query(
        Score,
        func.rank().over(
            order_by=Score.created_at.desc(),
            partition_by=Score.criterion_id
        ).label('rank')
    ).filter(Score.state == state).subquery()

    scores = db.session.query(subquery).filter(subquery.c.rank <= 1).all()
    serialized_scores = [score._asdict() for score in scores]

    for score in serialized_scores:
        score.pop('rank')
        score.pop('created_at')

    return {
        'links': links,
        'scores': serialized_scores
    }
