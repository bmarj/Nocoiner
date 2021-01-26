import json
from flask import Blueprint, redirect, request, url_for, config, flash, render_template
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from .business import get_user_by_id, get_user_by_username, authenticate_user
from .forms import LoginForm
#from . import um


bp = user_management = Blueprint('user_management', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')


# User session management setup
# https://flask-login.readthedocs.io/en/latest
class UserManager(LoginManager):
    def init_app(self, app):
        # registers blueprint into same url namespace as login manager
        app.register_blueprint(user_management, url_prefix='/')
        self.user_loader(self.load_user)
        self.unauthorized_handler(self.handle_unauthorized)
        super().init_app(app)

    def load_user(self, id):
        return get_user_by_id(id)

    def handle_unauthorized(self):
        return redirect(url_for('user_management.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/orders')
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user is None or not authenticate_user(form.username.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/orders')
    return render_template('login.jinja', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

