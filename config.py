import os
SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://Bruno@localhost:5432/menu-db-v1'
SQLALCHEMY_TRACK_MODIFICATIONS = False
