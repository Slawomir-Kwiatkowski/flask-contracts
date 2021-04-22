from flask_contracts import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    ''' Basic User Model '''
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    confirm_date = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(10))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    token_timestamp = db.Column(db.String(19), nullable=True)
    



# class UserWithLogo(User):
#     ''' User Model with Logo added '''
#     logo = db.Column(db.String(10), nullable=True)
