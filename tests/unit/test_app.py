def test_app_is_created(app):
    '''
    GIVEN an app instance
    WHEN a new flask app is created
    THEN check the app name
    '''
    assert app.name == 'flask_contracts'

def test_app_config(config):
    '''
    GIVEN a config of an app
    WHEN a new flask app is created
    THEN check config TESTING and DEBUG variables
    '''
    assert config['TESTING'] is True
    assert config['DEBUG'] is False