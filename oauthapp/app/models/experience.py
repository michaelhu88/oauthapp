from .. import db
from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime

class Experience(db.Model):
    __tablename__ = 'experience'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    companyName = db.Column(db.String(120))
    #this needs to be serialized
    timePeriod = db.Column(Text)
    description = db.Column(db.String(255))
    #serialize
    company = db.Column(Text)
    title = db.Column(db.String(120))
    entityUrn = db.Column(db.String(255))
    


