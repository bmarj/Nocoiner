from flask import Blueprint, session, jsonify, request, render_template
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError


from api.datatables import DataTables
from .business import update_order_line_flags, order_lines_query, get_order_lines_by_id, get_order_line_flags_by_id
from .schemas import (
    OrderFeedsSchema,
    UpdateOrderLineFlagsSchema)

orders = Blueprint('orders', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@orders.route("/")
def index():
    return render_template("dt.jinja")

@orders.route("/edit/<id>")
def edit(id):
    obj = get_order_lines_by_id(id)
    return render_template("edit_order_line.jinja", data=obj)

@orders.route("/dataDT")
def order_feedsDT():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = order_lines_query()

    # GET parameters
    params = request.args.to_dict()

    response_schema = OrderFeedsSchema(many=True)
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, response_schema)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@orders.route('/update', methods=['POST'])
def update():
    object_id = request.values.get("guid_order_line")
    input_data = request.values

    # first option:
    input_schema = UpdateOrderLineFlagsSchema()
    # fetch object from db
    update_obj = get_order_line_flags_by_id(object_id)

    # validate schema
    if input_schema.validate(input_data):
        obj = get_order_lines_by_id(object_id)
        return render_template("edit_order_line.jinja", data=obj)

    # update object with values
    oo = input_schema.load(input_data, instance=update_obj, partial=True, unknown=EXCLUDE)

    # commit to db
    update_obj.query.session.commit()
    return render_template("form_success.jinja")
