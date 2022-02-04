from flask_login import UserMixin
from . import db



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class ProjectData(UserMixin, db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key = True)
    prjname = db.Column(db.String(100))
    details = db.Column(db.String(1000))
   

    def __init__(self, id, prjname, details):
        self.id = id
        self.prjname = prjname
        self.details = details

    def __repr__(self) :
        return "{} is the project name and {} is the details".format(self.prjname,self.details)
