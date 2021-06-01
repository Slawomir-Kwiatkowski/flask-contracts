from datetime import datetime
from flask import (Blueprint, render_template, flash, redirect,
                    request, url_for, abort, current_app)
from flask_contracts import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from is_safe_url import is_safe_url
from .models import User
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserEmailForm,
                    UserChangePasswordForm
                    )
from .utils.utils import generate_token, check_token, send_email

bp = Blueprint('auth', __name__, url_prefix='/auth',
        template_folder='templates/auth', static_folder='static')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserRegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(role=form.role.data, username=form.username.data, email=form.email.data, password=hashed)
        timestamp = send_email(user.email, category='confirm_account')
        user.token_timestamp = timestamp
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}. A confirmation email has been sent.')
        return redirect(url_for('main.index'))
    return render_template('registration.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_active: return render_template('unconfirmed.html', title='Unconfirmed')
            login_user(user, remember=(not(form.log_out.data)))
            flash(f'Welcome: {user.username}!')
            next_param = request.args.get('next')
            host = current_app.config.get('FORCE_HOST_FOR_REDIRECTS')
            if next_param:
                if not is_safe_url(next_param, host):
                    return abort(400)
            return redirect(next_param or url_for('main.index'))
        else:
            flash('Bad credentials.')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You are signed out now!')
    return redirect(url_for('main.index'))


@bp.route('/confirm-account/<token>')
def confirm_account(token):
    if check_token(token): 
        email, timestamp = check_token(token)
        user = User.query.filter_by(email=str(email)).first()
        if user.token_timestamp == timestamp:
            user.is_active = True
            user.confirm_date = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            flash('Your account is now activated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid token.', 'warning')
            return render_template('unconfirmed.html', title='Unconfirmed')
    else:
        flash('Invalid or expired token.')
        return render_template('unconfirmed.html', title='Unconfirmed')


@bp.route('/resend-activation', methods=['GET', 'POST'])
def resend():
    form = UserEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            timestamp = send_email(user.email, category='confirm_account')
            user.token_timestamp = timestamp
            db.session.add(user)
            db.session.commit()
        flash('A confirmation email has been sent.') #safety reasons
        # The above flash msg will be displayed if user is or is not registered
        return redirect(url_for('main.index'))
    return render_template('resend_confirmation.html', title='Resend', form=form)
        

    
@bp.route('/forgot-credentials', methods=['GET', 'POST'])
def forgot_credentials():
    form = UserEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            timestamp = send_email(user.email, category='forgot_credentials')
            user.token_timestamp = timestamp
            db.session.add(user)
            db.session.commit()
        flash('An email has been sent with link to change credentials.', category='success') #safety reasons
        # The above flash msg will be displayed if user is or is not registered
        return redirect(url_for('main.index'))
    return render_template('forgot_credentials.html', title='Forgot Credentials', form=form)



@bp.route('/change-password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if not check_token(token):
        flash('Bad token')
        return redirect('main.index')
    email, timestamp = check_token(token)
    user = User.query.filter_by(email=str(email)).first()
    form = UserChangePasswordForm()
    if form.validate_on_submit():
        if user.token_timestamp == timestamp:
            hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed
            if not user.is_active:
                user.is_active = True
                user.confirm_date = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            flash('Password changed.')
            return redirect(url_for('auth.login'))
    return render_template('change_password.html', 
                title='Password Reset', username=user.username, form=form)

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_pass():
    form = UserChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed
        db.session.add(user)
        db.session.commit()
        flash('Password changed.')
        return redirect(url_for('main.index'))
    return render_template('change_password.html', 
            title='Password Reset', username=current_user.username, form=form)