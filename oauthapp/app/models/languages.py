from .. import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Languages(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    name = db.Column(db.String(120))
    proficiency = db.Column(db.String(120))
    