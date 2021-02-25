from datetime import datetime
from flask import (Blueprint, render_template, flash, redirect,
                    request, url_for, abort, current_app)
from flask_contracts import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from is_safe_url import is_safe_url
from .models import User
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserForgotCredentials,
                    UserChangePasswordForm
                    )
from .utils.utils import generate_token, check_token, send_email

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserRegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        token = generate_token(user.email)
        send_email(user.email, token, category='confirm_account')
        _, timestamp = check_token(token)
        user.token_timestamp = timestamp
        flash(f'Account created for {user.username}. A confirmation email has been sent.', category='success')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('registration.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user.is_active : return redirect(url_for('auth.unconfirmed_account'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=(not(form.log_out.data)))
            flash(f'Welcome: {user.username}!', 'success')
            next_param = request.args.get('next')
            host = current_app.config.get('FORCE_HOST_FOR_REDIRECTS')
            if next_param:
                if not is_safe_url(next_param, host):
                    return abort(400)
            return redirect(next_param or url_for('main.index'))
        else:
            flash('Bad credentials.', 'danger')
    return render_template('login.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You are signed out now!', 'info')
    return redirect(url_for('main.index'))


@bp.route('/confirm-account/<token>')
def confirm_account(token):
    email, timestamp = check_token(token)
    user = User.query.filter_by(email=str(email)).first()
    user.is_active = True
    user.confirm_date = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    flash('Your account is now activated.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/unonfirmed')
def unconfirmed_account():
    return 'Your account requires confirmation'

@bp.route('/forgot-credentials', methods=['GET', 'POST'])
def forgot_credentials():
    form = UserForgotCredentials()
    if form.validate_on_submit():
        flash('An e-mail was sent to the address provided.', category='info')
        return redirect(url_for('main.index'))
    return render_template('forgot-credentials.html', title='Forgot Credentials', form=form)

@bp.route('/change-password')
def change_password():
    if current_user.is_active:
        return 'active'
    else:
        return 'inactive'
    # form = UserRegisterForm()
    # if form.validate_on_submit():
    #     hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user = User(username=form.username.data, email=form.email.data, password=hashed)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash(f'Account created for {form.username.data}. You can sign in now.', category='success')
    #     return redirect(url_for('auth.login'))
    # return redirect(url_for('main.index'))