from .. import db
from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime

class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    timePeriod = db.Column(Text)
    description = db.Column(db.String(255))
    title = db.Column(db.String(120))
    url = db.Column(db.String(120))
    entityUrn = db.Column(db.String(255))