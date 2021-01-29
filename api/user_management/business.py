from werkzeug.security import generate_password_hash, check_password_hash
from .model import Permission, User, Role, RolePermission, UserRole


###
### Queries (to enable further server side processing like sorting, paging and filtering)
###
def query_users():
    # join to eager load relations
    q = User.query\
        .outerjoin(UserRole)\
        .outerjoin(Role)
    return q

def query_roles():
    # join to eager load relations
    q = Role.query
    return q

def query_user_roles():
    # join to eager load relations
    q = UserRole.query\
        .join(User)\
        .join(Role)
    return q

def query_role_permissions():
    # join to eager load relations
    q = RolePermission.query\
        .join(Role)\
        .join(Permission)
    return q

def query_permissions():
    # join to eager load relations
    q = Permission.query
    return q

###
### Fetch or process objects
###
def get_user_by_id(id):
    q = User.query\
        .get(int(id))
    return q

def get_user_by_username(username):
    q = User.query\
        .filter(User.username == username)\
        .filter(User.active == True)\
        .one_or_none()
    return q

def authenticate_user(username, password):
    q = User.query\
        .filter(User.username == username)\
        .filter(User.active == True)\
        .one_or_none()
    if q and check_password(q, password):
        return q
    return None


def set_password(id, password):
    q = get_user_by_id(id)
    password_hash = generate_password_hash(password)
    q.password = password_hash
    # commit to db
    q.db.session.commit()

def check_password(user: User, password):
    return check_password_hash(user.password, password)

def create_permission():
    q = Permission()
    return q

def get_permission_by_id(id):
    q = Permission.query\
        .get(int(id))
    return q

def create_role():
    q = Role()
    return q

def get_role_by_id(id):
    q = Role.query\
        .get(int(id))
    return q

def create_user_role():
    q = UserRole()
    return q

def get_user_role_by_id(id):
    q = UserRole.query\
        .get(int(id))
    return q


def create_role_permission():
    q = RolePermission()
    return q

def get_role_permission_by_id(id):
    q = RolePermission.query\
        .get(int(id))
    return q

def create_user():
    q = User()
    return q

# convenience methods for permssions and roles are also on User object

def get_user_permissions(id):
    """
    get user permissions from database
    """
    q = Permission.query\
        .join(RolePermission)\
        .join(Role)\
        .join(UserRole)\
        .filter(UserRole.app_user_id == int(id))\
        .all()
    return q

# def get_user_permissions_type2(id):
#     """
#     another filtering flavor
#     ( generates WHERE EXISTS type query )
#     """
#     q = Permission.query\
#         .filter(
#             Permission.role_permissions.any(
#             Role.user_roles.any(
#             UserRole.app_user_id == int(id)))
#         ).all()
#     return q
