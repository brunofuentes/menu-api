import os


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    # SECRET_KEY = os.urandom(32)
