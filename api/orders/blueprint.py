from flask import Blueprint, session, jsonify
from api.orders.schemas import db, Order, OrderLine, OrderDetailSchema
from api.basic_schemas import FulfillmentWarehouse, FulfillmentWarehouseSchema, OrderSchema
import marshmallow
from flask_sqlalchemy import orm

orders = Blueprint('orders', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')


@orders.route('/', methods=['GET'])
def index():
    response_schema = OrderDetailSchema(many=True)

    # eager loading order lines for orders
    o = Order.query\
        .options(orm.subqueryload(Order.order_lines))\
        .paginate(1, 200).items
    return jsonify(response_schema.dump(o))

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
    response_schema = OrderDetailSchema()
    o = Order.query.get_or_404(id)

    return jsonify(response_schema.dump(o))

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

@orders.route('/test/', methods=['GET'])
def test():
    return "test"

@orders.route('/failed500/', methods=['GET'])
def failed500():
    raise Exception()
