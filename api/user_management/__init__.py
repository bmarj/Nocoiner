from flask import redirect
from flask.helpers import url_for
from flask_login import LoginManager, login_required
from .business import get_user_by_id
from .blueprint import UserManager



um = UserManager()

# @um.user_loader
# def load_user(id):
#     return get_user_by_id(id)

# @um.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('user_management.login'))
