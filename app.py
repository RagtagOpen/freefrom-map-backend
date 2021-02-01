import strings
from auth import AuthError, requires_auth
import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import cross_origin

app = Flask(__name__)

load_dotenv()

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import services  # noqa: E402

from models import (  # noqa: E402
    Category,
    Criterion,
    Link,
    Score,
    State
)


@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify(description=str(e.description)), 400


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify(description=str(e)), 400


@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify(e.error), 401


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify(description=str(e.description)), 404


@app.errorhandler(405)
def handle_not_allowed(e):
    return jsonify(description=str(e.description)), 405


@app.errorhandler(Exception)
def handle_server_error(e):
    return jsonify(description='Internal server error'), 500


@app.route('/categories', methods=['GET'])
def get_categories():
    with_criteria = request.args.get('withCriteria') == 'true'

    categories = Category.query.all()
    return jsonify([category.serialize(with_criteria) for category in categories])


@app.route('/categories', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def create_category():
    data = request.get_json()
    category = services.update_or_create_category(data=data)
    return jsonify(category.serialize()), 201


@app.route('/categories/<id_>', methods=['GET'])
def get_category(id_):
    category = Category.query.get(id_)

    if category is None:
        abort(404, strings.category_not_found)

    with_criteria = request.args.get('withCriteria') == 'true'
    return jsonify(category.serialize(with_criteria))


@app.route('/categories/<id_>', methods=['PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def update_category(id_):
    category = Category.query.get(id_)
    data = request.get_json()

    if category is None:
        abort(404, strings.category_not_found)

    category = services.update_or_create_category(data, category=category)
    return jsonify(category.serialize())


@app.route('/criteria', methods=['GET'])
def get_criteria():
    criteria = Criterion.query.all()
    return jsonify([criterion.serialize() for criterion in criteria])


@app.route('/criteria', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def create_criterion():
    data = request.get_json()
    criterion = services.update_or_create_criterion(data=data)
    return jsonify(criterion.serialize()), 201


@app.route('/criteria/<id_>', methods=['GET'])
def get_criterion(id_):
    criterion = Criterion.query.get(id_)

    if criterion is None:
        abort(404, strings.criterion_not_found)

    return jsonify(criterion.serialize())


@app.route('/criteria/<id_>', methods=['PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def update_criterion(id_):
    criterion = Criterion.query.get(id_)

    if criterion is None:
        abort(404, strings.criterion_not_found)

    data = request.get_json()
    services.update_or_create_criterion(data, criterion)
    return jsonify(criterion.serialize())


@app.route('/links', methods=['GET'])
@app.route('/links')
def get_links():
    links = Link.query.all()
    return jsonify([link.serialize() for link in links])


@app.route('/links', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def create_link():
    data = request.get_json()
    link = services.update_or_create_link(data=data)
    return jsonify(link.serialize()), 201


@app.route('/links/<id_>', methods=['GET'])
def get_link(id_):
    link = Link.query.get(id_)

    if link is None:
        abort(404, strings.link_not_found)

    return jsonify(link.serialize())


@app.route('/links/<id_>', methods=['PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def update_link(id_):
    link = Link.query.get(id_)
    data = request.get_json()

    if link is None:
        abort(404, strings.link_not_found)

    link = services.update_or_create_link(data, link=link)
    return jsonify(link.serialize())


@app.route('/grades/<code_>', methods=['GET'])
def get_state_grades(code_):
    state = State.query.get(code_)

    if state is None:
        abort(404, strings.invalid_state)

    state_data = state.serialize()
    return jsonify(
        grade=state_data['grade'],
        category_grades=state_data['category_grades'],
    ), 200


@app.route('/scores', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def create_score():
    data = request.get_json()
    score = Score(
        criterion_id=data.get('criterion_id'),
        state=data.get('state'),
        meets_criterion=data.get('meets_criterion'),
    ).save()

    return jsonify(score.serialize()), 201


@app.route('/states/<code_>', methods=['GET'])
def get_state(code_):
    state = State.query.get(code_)

    if state is None:
        abort(404, strings.invalid_state)

    return jsonify(state.serialize()), 200


@app.route('/states', methods=['GET'])
def get_states():
    states = State.query.all()
    return jsonify([state.serialize() for state in states]), 200


@app.route('/forms/<name_>', methods=['POST'])
def submit_form(name_):
    data = request.get_json()
    form = services.submit_form_to_google(name_, data)
    return form, 201


# This doesn't need authentication
@app.route('/api/public')
@cross_origin(headers=['Content-Type', 'Authorization'])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


# This needs authentication
@app.route('/api/private')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def private():
    response = 'Hello from a private endpoint! You need to be authenticated to see this.'
    return jsonify(message=response)


if __name__ == '__main__':
    app.run()
