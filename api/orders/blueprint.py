from flask import Blueprint

orders = Blueprint('orders', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@orders.route('/test/', methods=['GET'])
def test():
    return "test"

@orders.route('/failed500/', methods=['GET'])
def failed500():
    raise Exception()
