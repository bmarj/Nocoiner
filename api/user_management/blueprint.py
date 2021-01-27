from functools import wraps
import json
from flask import Blueprint, redirect, request, jsonify, url_for, current_app, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_login.config import EXEMPT_METHODS

from api.datatables import DataTables
from .business import (
    get_user_by_id, 
    get_user_by_username, 
    authenticate_user, 
    get_user_permissions,
    query_users,
    query_roles,
    query_user_roles
)
from .schemas import (
    UserSchema,
    RoleSchema,
    UserRoleSchema
)
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
        user = get_user_by_id(id)
        return user

    def handle_unauthorized(self):
        if request.accept_mimetypes.best == 'application/json':
            return jsonify(success=False,
                        data={'login_required': True},
                        message='Authorize please to access this page.'), 401
        else:
            return redirect(url_for('user_management.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    go_to_page = current_app.config.get('HOME_PAGE', '/home')
    if current_user.is_authenticated:
        return redirect(go_to_page)
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user is None or not authenticate_user(form.username.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(go_to_page)
    return render_template('login.jinja', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@bp.route("/users")
@login_required
def users():
    return render_template("users.jinja")

@bp.route("/users_data")
@login_required
def users_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_users()
    response_schema = UserSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


def authorize(permission_key = None):
    """
    Authorize function with given permission_key.
    If permission_key is not provided, use automatic: full module name + function name
    """
    def check_authorization(func):
        @wraps(func)
        @login_required        
        def decorated_view(*args, **kwargs):
            if permission_key:
                permission_name = permission_key
            else:
                permission_name = func.__module__ + '.' + func.__name__         
            if not current_user.has_permission(permission_name):
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return check_authorization
