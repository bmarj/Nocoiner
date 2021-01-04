from flask import Blueprint, session, jsonify, request, render_template
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError


from api.datatables import DataTables
from api.models.combined import OrderLines, TbProducts
from api.models import combined as m
# from api.models import (
#     db, Order, OrderLine)
# from api.models.simple_schema import (
#     FulfillmentWarehouse, FulfillmentWarehouseSchema, OrderSchema)
from api.models.request_helpers import get_filter_json, get_sort_json, get_paging_json
from .business import get_order_lines, update_order_line_flags, order_lines_query
from .schemas import (
    OrderFeedsSchema,
    UpdateOrderLineFlagsSchema)

orders_dt = Blueprint('orders_dt', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

# @orders.route('/', methods=['GET'])
# def index():
#     response_schema = OrderDetailSchema(many=True)
#     # eager loading order lines for orders
#     o = Order.query.options(orm.subqueryload(Order.order_lines))\
#         .paginate(1, 200).items
#     return jsonify(response_schema.dump(o))

# @orders_dt.route("/")
# def home():
#     """Try to connect to database, and list available examples."""
#     return render_template("home.jinja", project="flask_tut")


@orders_dt.route("/")
def index():
    return render_template("dt.jinja")

@orders_dt.route("/data")
def order_feeds():

    results = get_order_lines(
        get_filter_json(),
        get_sort_json(),
        get_paging_json()
    )

    response_schema = OrderFeedsSchema(many=True)

    return jsonify(
        {'draw': int(request.args.get('draw')),
         'recordsFiltered': len(results.items),
         'recordsTotal': results.total,
         'data': response_schema.dump(results.items)}
    )

5
@orders_dt.route("/dataDT")
def order_feedsDT():

    """Return server side data."""
    # # defining columns
    # columns = [
    #     ColumnDT(User.id),
    #     ColumnDT(User.name),
    #     ColumnDT(Address.description),
    #     ColumnDT(User.created_at),
    # ]

    # defining the initial query depending on your purpose
    query = order_lines_query()

    # GET parameters
    params = request.args.to_dict()

    response_schema = OrderFeedsSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, response_schema)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@orders_dt.route('/order_feed_serverside', methods=['GET'])
def order_feed_serverside():

    results = get_order_lines(
        get_filter_json(),
        get_sort_json(),
        get_paging_json()
    )

    response_schema = OrderFeedsSchema(many=True)
    return jsonify(
        {'data': {'page': results.page,
                  'itemsPerPage': results.per_page,
                  'totalRecords': results.total,
                  'order_lines': response_schema.dump(results.items)}}
    )

@orders_dt.route('/update_flag', methods=['POST'])
def update_flag():
    object_id = request.values.get("guid_order_line")
    input_data = request.values

    # first option:
    input_schema = UpdateOrderLineSchema()
    # fetch object from db
    update_obj = OrderLine.query.get_or_404(object_id)
    # update object with values
    oo = input_schema.load(input_data, instance=update_obj, partial=True, unknown=EXCLUDE)
    # commit to db
    db.session.commit()

    return jsonify(
        {'data': {'submitted': 1, 'succeeded': 1, 'failed': 0}}
    )

    # # reference: https://realpython.com/flask-connexion-rest-api-part-2/#
    # # turn the passed in data into a db object
    # request_schema = UpdateOrderLineSchema()
    # update = request_schema.load(input_data, unknown=EXCLUDE)
    # # Set the id to the person we want to update
    # update.id = object_id
    # # merge the new object into the old and commit it to the db
    # db.session.merge(update)
    # db.session.commit()

    # return jsonify(
    #     {'data': {'submitted': 1, 'succeeded': 1, 'failed': 0}}
    # )

@orders_dt.route('/order/<int:id>', methods=['GET'])
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

@orders_dt.route('/order/<int:id>/update/', methods=['GET', 'POST'])
def order_update(id):
    request_schema = OrderSchema()
    response_schema = OrderDetailSchema()
    o = Order.query.get_or_404(id)

    return jsonify(response_schema.dump(o))

@orders_dt.route('/order/<int:id>/error/', methods=['GET', 'POST'])
def order_update_error(id):
    request_schema = OrderSchema()
    o = Order.query.get_or_404(id)

    # let's try to load OrderLine from Order data
    incompatible_schema = OrderLineSchema()
    # raises ValidationError because of missing required fields
    ols = incompatible_schema.loads(request_schema.dumps(o), unknown=EXCLUDE)
    # exception is handled by common exception handler endpoint
    return "This won't be returned"

@orders_dt.route('/warehouse/<int:id>', methods=['GET'])
def warehouse(id):
    response_schema = FulfillmentWarehouseSchema()
    o = FulfillmentWarehouse.query.get_or_404(id)
    return jsonify(response_schema.dump(o))

@orders_dt.route('/warehouses/', methods=['GET'])
def warehouses():
    response_schema = FulfillmentWarehouseSchema(many=True)
    o = FulfillmentWarehouse.query.all()
    return jsonify(response_schema.dump(o))
