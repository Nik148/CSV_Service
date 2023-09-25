import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    DB_URL = os.environ.get('DB_URL')
    SECRET_KEY = "dima&pidoras"
    JWT_ALGORITHM = "HS256"