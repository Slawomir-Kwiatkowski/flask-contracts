from flask import (Flask, Blueprint, url_for
)
from .config import *   # Dev Config class

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # # Register blueprints here
    # from .auth import auth
    # app.register_blueprint(auth.bp)
    from .auth import auth
    app.register_blueprint(auth.bp)
    
    return app


