from .extenstions import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Project(db.Model,UserMixin):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    prjname = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, prjname, description):
        self.prjname = prjname
        self.description = description
