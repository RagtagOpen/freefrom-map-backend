import datetime
from app import db
from sqlalchemy.orm import validates

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
    "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    active = db.Column(db.Boolean())
    help_text = db.Column(db.String())
    deactivated_at = db.Column(db.DateTime)

    def __init__(self, title, help_text):
        self.title = title
        self.active = True
        self.help_text = help_text

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'active': self.active,
            'help_text': self.help_text,
            'deactivated_at': self.deactivated_at
        }

    def deactivate(self):
        self.active = False
        self.deactivated_at = datetime.datetime.utcnow()

        return True

class Criterion(db.Model):
    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    title = db.Column(db.String())
    recommendation_text = db.Column(db.String())
    help_text = db.Column(db.String())
    active = db.Column(db.Boolean())
    deactivated_at = db.Column(db.DateTime)
    adverse = db.Column(db.Boolean())

    def __init__(self, category_id, title, recommendation_text, help_text, adverse):
        self.category_id = category_id
        self.title = title
        self.recommendation_text = recommendation_text
        self.help_text = help_text
        self.active = True
        self.adverse = adverse

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'recommendation_text': self.recommendation_text,
            'help_text': self.help_text,
            'active': self.active,
            'deactivated_at': self.deactivated_at,
            'adverse': self.adverse
        }

    def deactivate(self):
        self.active = False
        self.deactivated_at = datetime.datetime.utcnow()

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    criterion_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
    state = db.Column(db.String(), nullable=False)
    meets_criterion = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime)

    def __init__(self, criterion_id, state, meets_criterion):
        self.criterion_id = criterion_id
        self.state = state
        self.meets_criterion = meets_criterion
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @validates('state')
    def validate_state(self, key, value):
        assert value in states
        return value

    def serialize(self):
        return {
            'id': self.id,
            'criterion_id': self.criterion_id,
            'created_at': self.created_at,
            'state': self.state,
            'meets_criterion': self.meets_criterion,
        }

db.Index('state_criterion_created_at', Score.state, Score.criterion_id, Score.created_at)

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    state = db.Column(db.String(), nullable=False)
    text = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, category_id, state, text, url):
        self.category_id = category_id
        self.state = state
        self.text = text
        self.url = url

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @validates('state')
    def validate_state(self, key, value):
        assert value in states
        return value

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'state': self.state,
            'text': self.text,
            'url': self.url,
        }

db.Index('state_category', Link.state, Link.category_id)
