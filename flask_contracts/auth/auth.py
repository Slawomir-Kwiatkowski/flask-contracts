from flask import Blueprint, render_template
from .forms import UserRegisterForm, UserLoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/login')
def login():
    form = UserLoginForm()
    return render_template('login.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    pass

@bp.route('/register')
def register():
    form = UserRegisterForm()
    return render_template('registration.html', title='Register', form=form)