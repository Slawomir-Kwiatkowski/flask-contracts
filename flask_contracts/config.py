class Config:
    ''' Development Config class'''

    SECRET_KEY = 'dev'
    ENV = 'dev'
    DEBUG = True


class ConfigProduction(Config):
    ''' Prodction Config class'''
    DEBUG = False
    ENV = 'prod'


class ConfigTesting(Config):
    '''Testing Config class'''
    pass
