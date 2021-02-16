
import json
from flask import Blueprint, redirect, request, jsonify, url_for, current_app, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .anonymous_user import AnonymousUser
from .decorators import authorize
from ..utils.common import generic_edit, generic_delete, generic_add, generic_form_delete, generic_form_edit

from api.datatables import DataTables
from .business import (
    get_user_by_id,
    get_user_by_username,
    authenticate_user,
    query_users,
    query_roles,
    query_user_roles,
    query_role_permissions,
    query_permissions,
    create_user
    )
from .schemas import (
    UserSchema,
    RoleSchema,
    UserRoleSchema,
    RolePermissionSchema,
    PermissionSchema
)
from .forms import (
    LoginForm,
    PermissionForm,
    RoleForm,
    UserRoleForm,
    RolePermissionForm,
    UserForm)

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
        self.anonymous_user = AnonymousUser
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

@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
@login_required
def home():
    go_to_page = current_app.config.get('HOME_PAGE', '/home')
    return redirect(go_to_page)

@bp.route("/users")
@authorize('users')
def users():
    return render_template("users.jinja")

@bp.route("/users_data")
@authorize('users')
def users_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_users()
    response_schema = UserSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/roles")
@authorize('users')
def roles():
    return render_template("roles.jinja")

@bp.route("/roles_data")
@authorize('users')
def roles_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_roles()
    response_schema = RoleSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/user-roles")
@authorize('users')
def user_roles():
    return render_template("user_roles.jinja")

@bp.route("/user-roles-data")
@authorize('users')
def user_roles_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_user_roles()
    response_schema = UserRoleSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/role-permissions")
@authorize('users')
def role_permissions():
    return render_template("role_permissions.jinja")

@bp.route("/role-permissions-data")
@authorize('users')
def role_permissions_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_role_permissions()
    response_schema = RolePermissionSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/permissions")
@authorize('users')
def permissions():
    return render_template("permissions.jinja")

@bp.route("/permissions_data")
@authorize('users')
def permissions_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_permissions()
    response_schema = PermissionSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

# user editing
@bp.route('/user_add', methods=['GET', 'POST'])
@authorize('users')
def user_add():
    return generic_add(UserForm, 'user_add.jinja', url_for('.user_add'))

@bp.route('/user_edit/<id>', methods=['GET'])
@bp.route('/user_edit', methods=['POST'])
@authorize('users')
def user_edit(id=None):
    return generic_edit(UserForm, 'user_edit.jinja', url_for('.user_edit'), id)

@bp.route("/user_delete/<id>", methods=['POST'])
@authorize('users')
def user_delete(id):
    return generic_delete(UserForm, id)

# generic editing
@bp.route('/form_edit/<id>', methods=['GET'])
@bp.route('/form_edit', methods=['GET','POST'])
@authorize('users')
def form_edit(id=None):
    permitted_forms = [UserForm,
        RoleForm, UserRoleForm, PermissionForm, RolePermissionForm]
    return generic_form_edit(url_for('.form_edit'), permitted_forms, id)

@bp.route("/delete/<id>", methods=['POST'])
@authorize('users')
def form_delete(id):
    permitted_forms = [RoleForm, UserRoleForm, PermissionForm, RolePermissionForm]
    return generic_form_delete(permitted_forms, id)