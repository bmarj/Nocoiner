from flask import Blueprint, session, jsonify, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from .business import inventory_lines, get_inventory_line_by_id
from .schemas import (
    InventoryLinesSchema,
    UpdateInventoryItemSchema)
from .forms import InventoryForm, ChangeQuantityForm

inventory = Blueprint('inventory', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@inventory.route("/")
def index():
    return render_template("index.jinja")

@inventory.route("/inventory_lines_data")
def inventory_lines_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = inventory_lines()

    # GET parameters
    params = request.args.to_dict()

    response_schema = InventoryLinesSchema(many=True)
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, response_schema)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@inventory.route("/edit/<id>")
def edit(id):    
    obj = get_inventory_line_by_id(id)
    form = InventoryForm(obj=obj)
    return render_template("edit_inventory_item.jinja", form=form, key=id)

@inventory.route('/update', methods=['POST'])
def update():
    object_id = request.values.get("key")
    input_data = request.values
    
    form = InventoryForm(input_data)

    if form.validate_on_submit():
        obj = get_inventory_line_by_id(object_id)
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Inventory item saved', category="Success")
        return render_template("form_success.jinja")

    # additional processing or validation:    
    form.validation_summary = 'Fill all required fields'
    
    return render_template("edit_inventory_item.jinja", form=form, key=object_id, classes="was-validated")

@inventory.route("/change-quantity/<id>")
def change_quantity(id):    
    obj = get_inventory_line_by_id(id)
    form = ChangeQuantityForm(obj=obj)
    return render_template("edit_quantity.jinja", form=form, key=id)

@inventory.route('/update-quantity', methods=['POST'])
def update_quantity():
    object_id = request.values.get("key")
    input_data = request.values
    
    form = ChangeQuantityForm(input_data)
    
    if form.validate_on_submit():
        obj = get_inventory_line_by_id(object_id)
        # form.populate_obj(obj)  # dont load form values to object
        # update object manually
        obj.Qty += form.UpdatedQty.data
        obj.query.session.commit()
        flash(f'{form.UpdatedQty.data} items added', category="Success")
        return render_template("form_success.jinja")
    
    return render_template("edit_quantity.jinja", form=form, key=object_id, classes="was-validated")

@inventory.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):    
    obj = get_inventory_line_by_id(id)
    obj.Qty = 0
    obj.query.session.commit()
    flash('Quantity deleted', category="Success")
    return render_template("form_success.jinja")