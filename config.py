import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    DB_URL = os.environ.get('DB_URL')
    TEST_DB_URL = os.environ.get("TEST_DB_URL")
    TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
    SECRET_KEY = "78DKFsef32-g93hnf203jgf30"
    JWT_ALGORITHM = "HS256"