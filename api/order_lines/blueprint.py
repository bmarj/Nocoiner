from flask import Blueprint, session, jsonify, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from api.user_management import login_required, authorize
from .business import query_order_line, get_order_line_by_id, set_order_line_status
from .schemas import (
    OrderLinesSchema)
from .forms import OrderLineForm

order_lines = bp = Blueprint('order_lines', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')


@bp.route("/")
@authorize('order_lines')
def order_lines_view():
    return render_template("order_lines.jinja")

@bp.route("/order_lines_data")
@authorize('order_lines')
def order_lines_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_order_line()
    response_schema = OrderLinesSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/edit/<id>")
@authorize('order_lines')
#@permission_name('test')
def edit(id):    
    obj = get_order_line_by_id(id)
    form = OrderLineForm(obj=obj)
    return render_template("edit_order_line.jinja", form=form, key=id)

@bp.route('/update', methods=['POST'])
@authorize('order_lines')
def update():
    object_id = request.values.get("key")
    input_data = request.values
    
    form = OrderLineForm(input_data)

    if form.validate_on_submit():
        obj = get_order_line_by_id(object_id)
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Order line saved', category="Success")
        return render_template("form_success.jinja")

    # additional processing or validation:    
    form.validation_summary = 'Fill all required fields'
    
    return render_template("edit_order_line.jinja", form=form, key=object_id, classes="was-validated")

@bp.route("/cancel/<id>", methods=['POST'])
@authorize('order_lines')
def cancel_order(id):    
    obj = get_order_line_by_id(id)
    set_order_line_status(obj, 'CANCELLED')
    obj.query.session.commit()
    flash('Order line cancelled', category="Success")
    return render_template("form_success.jinja")
