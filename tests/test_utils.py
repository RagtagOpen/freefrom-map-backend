import models


def clear_database(db):
    db.session.query(models.Link).delete()
    db.session.query(models.Score).delete()
    db.session.query(models.StateCategoryGrade).delete()
    db.session.query(models.StateGrade).delete()
    db.session.query(models.Criterion).delete()
    db.session.query(models.Subcategory).delete()
    db.session.query(models.Category).delete()
    db.session.query(models.State).delete()
    db.session.commit()


def create_state(code='NY'):
    return models.State(code=code).save()


def create_category():
    return models.Category(
        title='Definition of Domestic Violence',
        help_text="This is how a state legally defines the term 'domestic violence'",
    ).save()


def create_subcategory(category_id):
    return models.Subcategory(
        category_id=category_id,
        title='Safe Work Environment',
        help_text='Subcategory help text',
    ).save()


def create_criterion(subcategory_id):
    return models.Criterion(
        subcategory_id=subcategory_id,
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


def create_state_grade(state_code):
    return models.StateGrade(
        state_code=state_code,
        grade=2,
    ).save()


def create_state_category_grade(state_code, category_id):
    return models.StateCategoryGrade(
        state_code=state_code,
        category_id=category_id,
        grade=1,
    ).save()


def create_link(subcategory_id, state):
    return models.Link(subcategory_id=subcategory_id, state=state).save()


def create_resource_link(subcategory_id, state):
    return models.ResourceLink(subcategory_id=subcategory_id, state=state).save()


def auth_headers():
    return {'Authorization': 'Bearer fake token'}
