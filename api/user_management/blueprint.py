
import json
from flask import Blueprint, redirect, request, jsonify, url_for, current_app, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .decorators import authorize


from api.datatables import DataTables
from .business import (
    get_user_by_id, 
    get_user_by_username, 
    authenticate_user, 
    get_user_permissions,
    query_users,
    query_roles,
    query_user_roles,
    query_role_permissions,
    query_permissions,
    create_permission,
    get_permission_by_id,
    create_role,
    get_role_by_id,
    create_user_role,
    get_user_role_by_id,
    create_role_permission,
    get_role_permission_by_id,
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



@bp.route('/add_permission', methods=['GET', 'POST'])
@authorize('users')
def add_permission():
    obj = create_permission()

    if request.method == 'GET':
        form = PermissionForm(obj=obj)
    else:
        form = PermissionForm(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    # additional processing or validation:    
    # form.validation_summary = 'Fill all required fields'
    
    return render_template("permission_add.jinja", form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))


@bp.route('/edit_permission/<id>', methods=['GET'])
@bp.route('/edit_permission', methods=['POST'])
@authorize('users')
def edit_permission(id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    obj = get_permission_by_id(object_id)

    if request.method == 'GET':        
        form = PermissionForm(obj=obj)
    else:
        form = PermissionForm(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    # additional processing or validation:    
    # form.validation_summary = 'Fill all required fields'
    #     
    return render_template("permission_edit.jinja", form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

@bp.route("/delete_permission/<id>", methods=['POST'])
@authorize('users')
def delete_permission(id):    
    obj = get_permission_by_id(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")



@bp.route('/add_role', methods=['GET', 'POST'])
@authorize('users')
def add_role():
    obj = create_role()

    if request.method == 'GET':
        form = RoleForm(obj=obj)
    else:
        form = RoleForm(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template("role_add.jinja", form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))


@bp.route('/edit_role/<id>', methods=['GET'])
@bp.route('/edit_role', methods=['POST'])
@authorize('users')
def edit_role(id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    obj = get_role_by_id(object_id)

    if request.method == 'GET':        
        form = RoleForm(obj=obj)
    else:
        form = RoleForm(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template("role_edit.jinja", form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

@bp.route("/delete_role/<id>", methods=['POST'])
@authorize('users')
def delete_role(id):    
    obj = get_role_by_id(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")



@bp.route('/add_user_role', methods=['GET', 'POST'])
@authorize('users')
def add_user_role():
    obj = create_user_role()

    if request.method == 'GET':
        form = UserRoleForm(obj=obj)
    else:
        form = UserRoleForm(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template("user_role_add.jinja", form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))


@bp.route('/edit_user_role/<id>', methods=['GET'])
@bp.route('/edit_user_role', methods=['POST'])
@authorize('users')
def edit_user_role(id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    obj = get_user_role_by_id(object_id)

    if request.method == 'GET':        
        form = UserRoleForm(obj=obj)
    else:
        form = UserRoleForm(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template("user_role_edit.jinja", form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

@bp.route("/delete_user_role/<id>", methods=['POST'])
@authorize('users')
def delete_user_role(id):    
    obj = get_user_role_by_id(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")


@bp.route('/add_role_permission', methods=['GET', 'POST'])
@authorize('users')
def add_role_permission():
    obj = create_role_permission()

    if request.method == 'GET':
        form = RolePermissionForm(obj=obj)
    else:
        form = RolePermissionForm(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template("role_permission_add.jinja", form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))


@bp.route('/edit_role_permission/<id>', methods=['GET'])
@bp.route('/edit_role_permission', methods=['POST'])
@authorize('users')
def edit_role_permission(id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    obj = get_role_permission_by_id(object_id)

    if request.method == 'GET':        
        form = RolePermissionForm(obj=obj)
    else:
        form = RolePermissionForm(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template("role_permission_edit.jinja", form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

@bp.route("/delete_role_permission/<id>", methods=['POST'])
@authorize('users')
def delete_role_permission(id):    
    obj = get_role_permission_by_id(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")


@bp.route('/add_user', methods=['GET', 'POST'])
@authorize('users')
def add_user():
    obj = create_user()

    if request.method == 'GET':
        form = UserForm(obj=obj)
    else:
        form = UserForm(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template("user_add.jinja", form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))


@bp.route('/edit_user/<id>', methods=['GET'])
@bp.route('/edit_user', methods=['POST'])
@authorize('users')
def edit_user(id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    obj = get_user_by_id(object_id)

    if request.method == 'GET':        
        form = UserForm(obj=obj)
    else:
        form = UserForm(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template("user_edit.jinja", form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

@bp.route("/delete_user/<id>", methods=['POST'])
@authorize('users')
def delete_user(id):    
    obj = get_user_by_id(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")
