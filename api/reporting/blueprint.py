from flask import Blueprint, session, jsonify, url_for, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import generic_edit, generic_form_edit, generic_form_delete
from .business import query_order_lines
from .schemas import (
    OrderLinesSchema,
    OrdersSchema)
#from .forms import OrderForm

bp = Blueprint('reports', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')

@bp.route("/report1")
def report1():
    return render_template("report1.jinja")

@bp.route("/report1_data")
def report1_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_order_lines()
    response_schema = OrderLinesSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
