from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000), nullable=False)
    completed = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime(timezone=True),  nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),  nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    todos = db.relationship('Todo', backref='user', lazy=True)


