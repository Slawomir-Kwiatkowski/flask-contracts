# import os
class Config:
    ''' Development Config class'''

    SECRET_KEY = 'dev'
    ENV = 'dev'
    DEBUG = True


class ConfigProduction(Config):
    ''' Prodction Config class'''
    # SECRET_KEY = os.environ('SECRET_KEY')
    ENV = 'prod'
    DEBUG = False


class ConfigTesting(Config):
    '''Testing Config class'''
    pass
