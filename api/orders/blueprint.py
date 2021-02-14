from flask import Blueprint, session, jsonify, url_for, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import generic_edit, generic_form_edit, generic_form_delete
from .business import query_orders, get_order_by_id, set_order_status
from .schemas import (
    OrdersSchema)
from .forms import OrderForm

bp = Blueprint('orders', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')

@bp.route("/")
@authorize('orders')
def orders_view():
    return render_template("orders.jinja")

@bp.route("/orders_data")
@authorize('orders')
def orders_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_orders()
    response_schema = OrdersSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/edit/<id>")
@authorize('orders')
def edit(id):
    obj = get_order_by_id(id)
    form = OrderForm(obj=obj)
    return render_template("edit_order_shipping.jinja",
                           submit_target = url_for('.update'),
                           form=form, key=id)

@bp.route('/update', methods=['POST'])
@authorize('orders')
def update():
    object_id = request.values.get("key")
    input_data = request.values
    
    form = OrderForm(input_data)

    if form.validate_on_submit():
        obj = get_order_by_id(object_id)
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Order saved', category="Success")
        return render_template("form_success.jinja")

    # additional processing or validation:
    form.validation_summary = 'Fill all required fields'
    
    return render_template("edit_order_shipping.jinja",
        submit_target = url_for('.update'),
        form=form, key=object_id, classes="was-validated")

@bp.route("/cancel/<id>", methods=['POST'])
@authorize('orders')
def cancel_order(id):
    obj = get_order_by_id(id)
    set_order_status(obj, 'CANCELLED')
    obj.query.session.commit()
    flash('Order cancelled', category="Success")
    return render_template("form_success.jinja")


@bp.route('/order_details/<id>', methods=['GET'])
@bp.route('/order_details', methods=['POST'])
@authorize('orders')
def order_details(id=None):
    return generic_edit(OrderForm, 'order_details.jinja', url_for('.order_details'), id)


# generic editing
# need to change only permited forms
@bp.route('/form_edit/<id>', methods=['GET'])
@bp.route('/form_edit', methods=['GET','POST'])
@authorize('orders')
def form_edit(id=None):
    permitted_forms = [OrderForm]
    return generic_form_edit(url_for('.form_edit'), permitted_forms, id)

@bp.route("/delete/<id>", methods=['POST'])
@authorize('orders')
def form_delete(id):
    permitted_forms = [OrderForm]
    return generic_form_delete(permitted_forms, id)
