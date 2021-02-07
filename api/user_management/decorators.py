from functools import wraps
from flask import current_app
from flask_login import login_required, current_user


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