from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User


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