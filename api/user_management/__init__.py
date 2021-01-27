from flask_login import login_required
from .blueprint import UserManager, authorize


um = UserManager()
