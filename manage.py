from sys import argv
from getpass import getpass
from flask_contracts import create_app, db, bcrypt
from flask_contracts.config import Config, ConfigProduction, ConfigTesting
from flask_contracts.auth.models import User

app = create_app(Config) 


def create_db():
    app.app_context().push()
    db.create_all()

def create_admin():
    app.app_context().push()
    username = input('Enter admin name: ')
    email = input('Enter admin email: ')
    password = getpass('Enter admin password: ')
    confirm_password = getpass('Retype admin password: ')
    # Simple validation here:
    if '' in (username, email, password, confirm_password): raise ValueError('Empty value occurred')
    if password != confirm_password: raise ValueError("Passwords don't match")
    if User.query.filter_by(username=username).first(): raise ValueError('User already exists in db')

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    admin = User(username=username, email=email, password=hashed, admin=True, confirmed=True)
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    if len(argv) == 2:
        _, command = argv
        if command == 'run': app.run()
        if command == 'create_db': create_db()
        if command == 'create_admin': create_admin()

    else:
        print('Invalid command.')