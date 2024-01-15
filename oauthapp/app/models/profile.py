from .. import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    summary = db.Column(db.Text)
    industryName = db.Column(db.String(255))
    lastName = db.Column(db.String(120))
    locationName = db.Column(db.String(255))
    geoCountryName = db.Column(db.String(255))
    firstName = db.Column(db.String(120))
    geoLocationName = db.Column(db.String(255))
    headline = db.Column(db.String(255))
    displayPictureUrl = db.Column(db.String(255))
    public_id = db.Column(db.String(120))
    # Relationships
    experiences = db.relationship('Experience', backref='profile', lazy=True, cascade="all, delete-orphan")
    educations = db.relationship('Education', backref='profile', lazy=True, cascade="all, delete-orphan")
    languages = db.relationship('Languages', backref='profile', lazy=True, cascade="all, delete-orphan")
    projects = db.relationship('Projects', backref='profile', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Profile {self.linkedin_id}>'
