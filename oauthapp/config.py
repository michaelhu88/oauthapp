import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration variables
class Config:
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    DATA_DIR = "linkedin_data"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False

