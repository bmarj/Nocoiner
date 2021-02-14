from flask import Blueprint

bp = Blueprint('monitor', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')

@bp.route('/', methods=['GET'])
def check():
    return "ok", 200
