from flask import Blueprint

checks = Blueprint('checks', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@checks.route('/ok/', methods=['GET'])
def test():
    return "ok", 200

@checks.route('/failed500/', methods=['GET'])
def failed500():
    raise Exception()
