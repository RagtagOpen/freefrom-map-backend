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
from services import update_or_create_category, update_or_create_link

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
    return jsonify(error=404, text="Category does not exist"), 404

  return  jsonify(category.serialize())

@app.route("/categories/<id_>", methods=["PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_category(id_):
  category=Category.query.filter_by(id=id_).first()

  if category is None:
    return jsonify(error=404, text="Category does not exist"), 404

  category = update_or_create_category(category=category, data=request.form)
  db.session.add(category)
  db.session.commit()

  return  jsonify(category.serialize())

@app.route("/criteria")
def get_criteria():
	try:
		criteria=Criterion.query.all()
		return  jsonify([criterion.serialize() for criterion in criteria])
	except Exception as e:
		return(str(e))

@app.route("/criteria/<id_>")
def get_criterion(id_):
	try:
		criterion=Criterion.query.filter_by(id=id_).first()

		if criterion is None:
			return jsonify(error=404, text="Criterion does not exist"), 404

		return  jsonify(criterion.serialize())
	except Exception as e:
		return(str(e))

@app.route("/links", methods=["GET"])
def get_links():
	links=Link.query.all()
	return  jsonify([link.serialize() for link in links])

@app.route("/links", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_link():
  data = request.form
  link = update_or_create_link(data=data)
  db.session.add(link)
  db.session.commit()

  return jsonify(link.serialize()), 201

@app.route("/links/<id_>", methods=["GET"])
def get_link(id_):
	link=Link.query.filter_by(id=id_).first()

	if link is None:
		return jsonify(error=404, text="Link does not exist"), 404

	return  jsonify(link.serialize())

@app.route("/links/<id_>", methods=["PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def update_link(id_):
  link=Link.query.filter_by(id=id_).first()

  if link is None:
    return jsonify(error=404, text="Lategory does not exist"), 404

  link = update_or_create_link(link=link, data=request.form)
  db.session.add(link)
  db.session.commit()

  return  jsonify(link.serialize())

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
