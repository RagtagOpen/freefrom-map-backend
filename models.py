import datetime
from app import db
from sqlalchemy.orm import validates
import strings


class BaseMixin():
    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception
        return self

    @classmethod
    def save_all(cls, objects):
        db.session.add_all(objects)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception
        return objects


class Deactivatable(object):
    active = db.Column(db.Boolean())
    deactivated_at = db.Column(db.DateTime)

    def deactivate(self):
        self.active = False
        self.deactivated_at = datetime.datetime.utcnow()


class State(BaseMixin, db.Model):
    __tablename__ = 'states'

    code = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String())
    innovative_idea = db.Column(db.String())
    honorable_mention = db.Column(db.String())
    scores = db.relationship('Score', lazy=True)
    links = db.relationship('Link', lazy=True)

    def __init__(self, code, name=None, innovative_idea=None, honorable_mention=None):
        self.code = code
        self.name = name
        self.innovative_idea = innovative_idea
        self.honorable_mention = honorable_mention

    def __repr__(self):
        return '<id {}>'.format(self.code)

    def serialize(self):
        links = [link.serialize() for link in self.links if link.active]
        scores = []

        for criterion in Criterion.query.all():
            score = Score.query.filter_by(
                criterion_id=criterion.id,
                state=self.code,
            ).order_by(Score.created_at.desc()).first()
            if score:
                scores.append(score.serialize())

        return {
            'code': self.code,
            'name': self.name,
            'innovative_idea': self.innovative_idea,
            'honorable_mention': self.honorable_mention,
            'links': links,
            'scores': scores,
        }


class Category(BaseMixin, Deactivatable, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    help_text = db.Column(db.String())
    criteria = db.relationship('Criterion', backref='category', lazy=True)

    def __init__(self, title=None, help_text=None):
        self.title = title
        self.active = True
        self.help_text = help_text

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, with_criteria=False):
        data = {
            'id': self.id,
            'title': self.title,
            'active': self.active,
            'help_text': self.help_text,
            'deactivated_at': self.deactivated_at,
        }

        if with_criteria:
            data['criteria'] = [criterion.serialize() for criterion in self.criteria]

        return data


class Criterion(BaseMixin, Deactivatable, db.Model):
    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    title = db.Column(db.String())
    recommendation_text = db.Column(db.String())
    help_text = db.Column(db.String())
    adverse = db.Column(db.Boolean())

    def __init__(
        self, category_id, title=None, recommendation_text=None, help_text=None, adverse=None,
    ):
        self.category_id = category_id
        self.title = title
        self.recommendation_text = recommendation_text
        self.help_text = help_text
        self.active = True
        self.adverse = adverse

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @validates('category_id')
    def validate_category(self, key, value):
        if Category.query.get(value) is None:
            raise ValueError(strings.category_not_found)
        return value

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'recommendation_text': self.recommendation_text,
            'help_text': self.help_text,
            'active': self.active,
            'deactivated_at': self.deactivated_at,
            'adverse': self.adverse,
        }


class Score(BaseMixin, db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criteria.id'), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey('states.code'), nullable=False)
    meets_criterion = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime)

    def __init__(self, criterion_id, state, meets_criterion):
        self.criterion_id = criterion_id
        self.state = state
        self.meets_criterion = meets_criterion
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @validates('criterion_id')
    def validate_criterion(self, key, value):
        if Criterion.query.get(value) is None:
            raise ValueError(strings.criterion_not_found)
        return value

    @validates('state')
    def validate_state(self, key, value):
        if State.query.get(value) is None:
            raise ValueError(strings.invalid_state)
        return value

    def serialize(self):
        return {
            'id': self.id,
            'criterion_id': self.criterion_id,
            'state': self.state,
            'meets_criterion': self.meets_criterion,
        }


db.Index('state_criterion_created_at', Score.state, Score.criterion_id, Score.created_at)


class Link(BaseMixin, Deactivatable, db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    state = db.Column(db.String(2), db.ForeignKey('states.code'), nullable=False)
    text = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, category_id, state, text=None, url=None):
        self.category_id = category_id
        self.state = state
        self.text = text
        self.url = url
        self.active = True

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @validates('category_id')
    def validate_category(self, key, value):
        if Category.query.get(value) is None:
            raise ValueError(strings.category_not_found)
        return value

    @validates('state')
    def validate_state(self, key, value):
        if State.query.get(value) is None:
            raise ValueError(strings.invalid_state)
        return value

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'state': self.state,
            'text': self.text,
            'url': self.url,
            'active': self.active,
            'deactivated_at': self.deactivated_at,
        }


db.Index('state_category', Link.state, Link.category_id)
