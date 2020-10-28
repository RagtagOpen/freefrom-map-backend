from app import db

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

