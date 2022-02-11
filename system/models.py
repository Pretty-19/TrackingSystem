from .extenstions import db
from datetime import datetime
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


class Bug(db.Model,UserMixin):
    __tablename__ = "buglist"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    #AssignedTo = db.Column(db.String(20), nullable=False)
    #Createdby= db.Column(db.Integer, db.ForeignKey('user.AccessToken'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Type=db.Column(db.String(100),nullable=False)
    Priority=db.Column(db.String(100),nullable=False)
    Status = db.Column(db.String(100),nullable=False)


    def __repr__(self):
    	return "Bug('{}','{}','{}', '{}','{}','{}','{}')".format(self.id,self.title,self.date_posted,self.Createdby,self.Type,self.Priority,self.Status)