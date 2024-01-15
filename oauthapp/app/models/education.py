from .. import db
from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime


class Education(db.Model):
    __tablename__ = 'education'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    timePeriod = db.Column(Text)
    degreeName = db.Column(db.String(120))
    schoolName = db.Column(db.String(120))

