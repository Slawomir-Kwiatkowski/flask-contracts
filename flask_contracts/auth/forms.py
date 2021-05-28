from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_contracts.auth.models import User

class UserLoginForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=10)],
            description='Enter your username', render_kw={'autofocus': True})
    password = PasswordField('Password',
            validators=[DataRequired()],
            description='Enter your password')
    log_out = BooleanField('Log Me Out After', default=False)
    submit = SubmitField('Sign In')


class UserRegisterForm(UserLoginForm):
    email = EmailField('Email',
            validators=[DataRequired(), Email()],
            description='Enter your email')
    confirm_password = PasswordField('Confirm password',
            validators=[DataRequired(), EqualTo('password')],
            description='Confirm your password')
    role = SelectField('Role',
     choices=[('contractor', 'contractor'), ('customer', 'customer')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
            if User.query.filter_by(username=username.data).first():
                    raise ValidationError('This username is already taken.')

    def validate_email(self, email):
            if User.query.filter_by(email=email.data).first():
                    raise ValidationError('This email is already taken.')


class UserEmailForm(FlaskForm):
        email = EmailField('Email',
            validators=[DataRequired(), Email()],
            description='Enter your email')
        submit = SubmitField('Send')


class UserChangePasswordForm(FlaskForm):
        password = PasswordField('Password',
            validators=[DataRequired()],
            description='Enter your password')
        confirm_password = PasswordField('Confirm password',
                validators=[DataRequired(), EqualTo('password')],
                description='Confirm your password')
        submit = SubmitField('Change')
        

