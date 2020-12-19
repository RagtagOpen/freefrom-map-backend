import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import cross_origin

app = Flask(__name__)

load_dotenv()

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Category, Criterion, Link, Score
from auth import AuthError, requires_auth
from services import update_or_create_category, update_or_create_criterion
import strings

@app.errorhandler(AuthError)
def handle_auth_error(ex):
	response = jsonify(ex.error)
	response.status_code = ex.status_code
	return response

@app.route("/categories", methods=["GET"])
def get_categories():
    categories=Category.query.all()
    return  jsonify([category.serialize() for category in categories])

@app.route("/categories", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_category():
  data = request.form
  category = update_or_create_category(data=data)
  db.session.add(category)
  db.session.commit()

  return jsonify(category.serialize()), 201

@app.route("/categories/<id_>", methods=["GET"])
def get_category(id_):
  category=Category.query.filter_by(id=id_).first()

  if category is None:
    return jsonify(error=404, text=strings.category_not_found), 404

  return  jsonify(category.serialize())

@app.route("/categories/<id_>", methods=["PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_category(id_):
  category=Category.query.filter_by(id=id_).first()

  if category is None:
    return jsonify(error=404, text=strings.category_not_found), 404

  category = update_or_create_category(category=category, data=request.form)
  db.session.add(category)
  db.session.commit()

  return  jsonify(category.serialize())

@app.route("/criteria", methods=["GET"])
def get_criteria():
	try:
		criteria=Criterion.query.all()
		return  jsonify([criterion.serialize() for criterion in criteria])
	except Exception as e:
		return(str(e))

@app.route("/criteria", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_criterion():
  try:
    data = request.get_json()

    category = Category.query.filter_by(id=data.get('category_id')).first()
    if category is None:
      return jsonify(text=strings.category_not_found), 404

    criterion = update_or_create_criterion(data=data)
    db.session.add(criterion)
    db.session.commit()

    return jsonify(criterion.serialize()), 201

  except Exception as e:
    return jsonify(text=str(e)), 500

@app.route("/criteria/<id_>", methods=["GET"])
def get_criterion(id_):
	try:
		criterion=Criterion.query.filter_by(id=id_).first()

		if criterion is None:
			return jsonify(text=strings.criterion_not_found), 404

		return  jsonify(criterion.serialize())
	except Exception as e:
		return(str(e))

@app.route("/criteria/<id_>", methods=["PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_criterion(id_):
  try:
    criterion = Criterion.query.filter_by(id=id_).first()

    if criterion is None:
      return jsonify(text=strings.criterion_not_found), 404

    data = request.get_json()

    category_id = data.get('category_id')
    if category_id and category_id != criterion.category_id:
      return jsonify(text=strings.criterion_cannot_change_category), 400

    update_or_create_criterion(data, criterion)
    db.session.add(criterion)
    db.session.commit()

    return jsonify(criterion.serialize())

  except Exception as e:
    return jsonify(text=str(e)), 500

@app.route("/links")
def get_links():
	try:
		links=Link.query.all()
		return  jsonify([link.serialize() for link in links])
	except Exception as e:
		return(str(e))

@app.route("/links/<id_>")
def get_link(id_):
	try:
		link=Link.query.filter_by(id=id_).first()

		if link is None:
			return jsonify(error=404, text="Link does not exist"), 404

		return  jsonify(link.serialize())
	except Exception as e:
		return(str(e))

# This doesn't need authentication
@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)

# This needs authentication
@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

if __name__ == '__main__':
		app.run()
