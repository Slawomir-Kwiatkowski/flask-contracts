from flask_contracts import create_app
from flask_contracts.config import Config, ConfigProduction

if __name__ == '__main__':
    app = create_app(Config)
    app.run()
