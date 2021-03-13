import pytest
from flask_contracts import create_app
from flask_contracts.config import ConfigTesting

@pytest.fixture(scope='module')
def app():
    ''' Main app instance '''
    return create_app(ConfigTesting)