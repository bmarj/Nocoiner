from flask_login import login_required
from .decorators import authorize
from .blueprint import UserManager


um = UserManager()
