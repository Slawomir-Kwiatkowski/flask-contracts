import os

class Config:
    ''' Development Config class'''
    SECRET_KEY = 'dev'
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FORCE_HOST_FOR_REDIRECTS = 'localhost:5000'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = 'noreplay'

class ConfigProduction(Config):
    ''' Prodction Config class'''
    # SECRET_KEY = os.environ('SECRET_KEY')
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigTesting(Config):
    '''Testing Config class'''
    SECRET_KEY = 'dev'
    ENV = 'test'
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'file::memory:?cache=shared'
    SQLALCHEMY_TRACK_MODIFICATIONS = False