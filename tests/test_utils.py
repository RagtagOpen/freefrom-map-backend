import models


def clear_database(db):
    db.session.query(models.Link).delete()
    db.session.query(models.Score).delete()
    db.session.query(models.Criterion).delete()
    db.session.query(models.Category).delete()
    db.session.commit()


def create_category():
    return models.Category(
        title='Definition of Domestic Violence',
        help_text="This is how a state legally defines the term 'domestic violence'",
    ).save()


def create_criterion(category_id):
    return models.Criterion(
        category_id=category_id,
        title='Includes economic abuse framework',
        recommendation_text=(
            "The state's definition of domestic violence should include a framework of economic "
            'abuse'
        ),
        help_text=(
            'This means that the state acknowledges the role that economic control and abuse can '
            'play in domestic violence'
        ),
        adverse=False
    ).save()

def create_link(category_id):
    return models.Link(category_id=category.id)


def auth_headers():
    return {'Authorization': 'Bearer fake token'}
