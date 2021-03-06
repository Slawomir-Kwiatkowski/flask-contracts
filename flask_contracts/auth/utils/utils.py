from flask import current_app, Blueprint, render_template, url_for
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_mail import Message
from flask_contracts import mail

bp = Blueprint('utils', __name__, template_folder='templates/utils')

def generate_token(email):
    serializer = Serializer(current_app.config.get('SECRET_KEY'))
    token = serializer.dumps(email)
    return token

def check_token(token, expiration=7200, return_timestamp=True):
    serializer = Serializer(current_app.config.get('SECRET_KEY'))
    try:
        email, timestamp = serializer.loads(token, max_age=expiration, return_timestamp=True)
    except (BadSignature, SignatureExpired):
        return None
    return (email, str(timestamp))

def send_email(email, category=None):
    token = generate_token(email)
    if category == 'confirm_account':
        subject = 'Please confirm your account'
        html = render_template('confirm_account.html',
                    title='Email Confirmation',
                    token=token )
        message = Message(subject, recipients=[email], html=html)
        mail.send(message)
    if category == 'forgot_credentials':
        subject = 'Reset account credentials'
        html = render_template('change_credentials.html',
                    title='Password Reset',
                    token=token )
        message = Message(subject, recipients=[email], html=html)
        mail.send(message)

    _, timestamp = check_token(token)
    return timestamp

    