import os


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/menu-db-v1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(32)
