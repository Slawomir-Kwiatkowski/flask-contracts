class Config:
    ''' Development Config class'''

    SECRET_KEY = 'dev'
    ENV = 'dev'
    DEBUG = True


class ConfigProduction(Config):
    ''' Prodction Config class'''
    ENV = 'prod'
    DEBUG = False


class ConfigTesting(Config):
    '''Testing Config class'''
    pass
