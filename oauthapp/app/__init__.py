from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.from_object('config.Config')

db = SQLAlchemy(app)

from .models import *

from .views import *

with app.app_context():
    db.drop_all()
    db.create_all()

