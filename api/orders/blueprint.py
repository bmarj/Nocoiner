from flask import Blueprint, session, jsonify
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError

from api.models import (
    db, Order, OrderLine)
from api.simple_schema import (
    FulfillmentWarehouse, FulfillmentWarehouseSchema, OrderSchema)
from api.orders.schemas import (
    OrderDetailSchema, OrderLineSchema, OrderFeedsSchema)

orders = Blueprint('orders', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@orders.route('/', methods=['GET'])
def index():
    response_schema = OrderDetailSchema(many=True)
    # eager loading order lines for orders
    o = Order.query.options(orm.subqueryload(Order.order_lines))\
        .paginate(1, 200).items
    return jsonify(response_schema.dump(o))


@orders.route('/order_feed_serverside', methods=['GET'])
def orderList():
    response_schema = OrderFeedsSchema(many=True)
    # eager loading order lines for orders
    q = OrderLine.query

    return jsonify(
        {'data': {'itemsPerPage': 10, 'page': 1, 'totalRecords': q.count(),
                  'order_lines':
                  response_schema.dump(q.paginate(1, 10).items)}}
    )

@orders.route('/order/<int:id>', methods=['GET'])
def order(id):
    response_schema = OrderDetailSchema()
    o = Order.query.get_or_404(id)

    # o = Order.query.filter_by(id=id).one()
    # Order.query.filter_by(ship_city='APO').all()
    # o = Order.query.filter(Order.ship_city == 'APO').all()
    # o = Order.query.filter_by(ship_city='APO').first_or_404()
    # order = response_schema.load(o)
    # from marshmallow import pprint
    # pprint(response_schema.dump(o))
    return jsonify(response_schema.dump(o))

@orders.route('/order/<int:id>/update/', methods=['GET', 'POST'])
def order_update(id):
    request_schema = OrderSchema()
    response_schema = OrderDetailSchema()
    o = Order.query.get_or_404(id)

    return jsonify(response_schema.dump(o))

@orders.route('/order/<int:id>/error/', methods=['GET', 'POST'])
def order_update_error(id):
    request_schema = OrderSchema()
    o = Order.query.get_or_404(id)

    # let's try to load OrderLine from Order data
    incompatible_schema = OrderLineSchema()
    # raises ValidationError because of missing required fields
    ols = incompatible_schema.loads(request_schema.dumps(o), unknown=EXCLUDE)
    # exception is handled by common exception handler endpoint
    return "This won't be returned"

@orders.route('/warehouse/<int:id>', methods=['GET'])
def warehouse(id):
    response_schema = FulfillmentWarehouseSchema()
    o = FulfillmentWarehouse.query.get_or_404(id)
    return jsonify(response_schema.dump(o))

@orders.route('/warehouses/', methods=['GET'])
def warehouses():
    response_schema = FulfillmentWarehouseSchema(many=True)
    o = FulfillmentWarehouse.query.all()
    return jsonify(response_schema.dump(o))
