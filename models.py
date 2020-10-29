import datetime
from app import db
from sqlalchemy.orm import validates

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    active = db.Column(db.Boolean())

    def __init__(self, title, active):
        self.title = title
        self.active = active

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'active': self.active,
        }

class Criterion(db.Model):
    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    title = db.Column(db.String())
    recommendation_text = db.Column(db.String())
    active = db.Column(db.Boolean())

    def __init__(self, category_id, title, recommendation_text, active):
        self.category_id = category_id
        self.title = title
        self.recommendation_text = recommendation_text
        self.active = active

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'recommendation_text': self.recommendation_text,
            'active': self.active,
        }
        
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
        assert value in ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", 
             "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", 
             "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
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
