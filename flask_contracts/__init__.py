from flask import (Flask, Blueprint, url_for
)
from .config import *   # Dev Config class
from flask_fontawesome import FontAwesome

fa = FontAwesome()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    fa.init_app(app)

    # # Register blueprints here
    from .auth import auth
    app.register_blueprint(auth.bp)
    
    return app


