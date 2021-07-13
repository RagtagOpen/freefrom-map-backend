from models import (
    Category,
    Criterion,
    State,
)

from services import (
    update_or_create_category,
    update_or_create_criterion,
    update_state
)


def import_categories(categories_json):
    return list(map(import_category, categories_json))


def import_states(states_json):
    return list(map(import_state, states_json))


def import_category(category_json):
    category = Category.query.get(category_json['id'])

    category = update_or_create_category(category_json, category)

    for criterion_json in category_json['criteria']:
        criterion_json['category_id'] = category_json['id']
        import_criterion(criterion_json, category_json['id'])

    return category.serialize(with_criteria=True)


def import_criterion(criterion_json, category_id):
    criterion = Criterion.query.get(criterion_json['id'])
    criterion = update_or_create_criterion(criterion_json, criterion=criterion)

    return criterion.serialize()


def import_state(state_json):
    state = State.query.get(state_json['code'])

    if state is None:
        raise Exception(f'{state_json["code"]} is not a valid state code')

    state = update_state(state_json, state)

    return state.serialize()
