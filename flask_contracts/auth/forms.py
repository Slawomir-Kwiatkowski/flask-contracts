from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class UserLoginForm(FlaskForm):
    username = StringField('username',
            validators=[DataRequired(), Length(min=1, max=10)],
            description='Enter your username')
    password = PasswordField('Password',
            validators=[DataRequired()],
            description='Enter your password')
    log_out = BooleanField('Log Me Out After', default='checked')
    submit = SubmitField('Sign In')

class UserRegisterForm(UserLoginForm):
    email = EmailField('Email',
            validators=[DataRequired(), Email()],
            description='Enter your email')
    confirm_password = PasswordField('Confirm password',
            validators=[DataRequired(), EqualTo('password')],
            description='Confirm your password')
    submit = SubmitField('Sign Up')

