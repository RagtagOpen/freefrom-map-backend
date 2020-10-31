import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Category, Criterion, Score

@app.route("/categories")
def get_categories():
	try:
		categories=Category.query.all()
		return  jsonify([category.serialize() for category in categories])
	except Exception as e:
		return(str(e))

@app.route("/categories/<id_>")
def get_category(id_):
	try:
		category=Category.query.filter_by(id=id_).first()

		if category is None:
			return jsonify(error=404, text="Category does not exist"), 404

		return  jsonify(category.serialize())
	except Exception as e:
		return(str(e))

if __name__ == '__main__':
		app.run()
