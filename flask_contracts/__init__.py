from flask import Flask
from .config import *   # Config classes
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# Apps:
fa = FontAwesome()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class):
    # Flask config section
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init apps section
    fa.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # apps config section
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    

    # # Register blueprints section
    from . import flask_contracts
    from .auth import auth
    from .auth.utils import utils
    from .contracts import contracts
    app.register_blueprint(flask_contracts.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(utils.bp)
    app.register_blueprint(contracts.bp)
    
    return app


