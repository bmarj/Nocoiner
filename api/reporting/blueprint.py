from flask import Blueprint, session, jsonify, url_for, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError
from sqlalchemy.sql import select, desc
from sqlalchemy.orm import object_session
from sqlalchemy import func, bindparam

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import generic_edit, generic_form_edit, generic_form_delete
from .model import OrderView, InventoryView
from .schemas import (
    OrderViewSchema,
    InventoryViewSchema)
#from .forms import OrderForm

bp = Blueprint('reports', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')


@bp.route("/report1")
def report1():
    return render_template("report1.jinja")

@bp.route("/report1_data")
def report1_data():
    """Sales by Country table data.
    """

    # # defining the initial query depending on your purpose
    # query = query_order_lines()
    response_schema = OrderViewSchema(many=True)

    # query = select([
    #     OrderView.ship_country,
    #     func.sum(OrderView.qty_ordered).label('qty_ordered'),
    #     #func.count().label('total_volume'),
    # ]).group_by(
    #         OrderView.ship_country,
    # )

    t = OrderView
    dbsession = OrderView.query.session

    ## aggregates defined in query work this way
    # query = dbsession.query(t.ship_country, t.sum_qty_ordered,
    #                         func.sum(t.qty_shipped).label('sum_qty_shipped'),
    #                         func.sum(t.qty_ordered).label('sum_qty_ordered')
    #                        ).group_by(t.ship_country).having(func.sum(t.qty_ordered) > 3000).order_by(desc(func.sum(t.qty_ordered)))

    # aggregates defined in model have advantage of sorting by that columns
    query = dbsession.query(t.ship_country,
                            t.sum_qty_shipped,
                            t.sum_qty_ordered,
                            t.sum_price,
                           ).group_by(t.ship_country)
                            #.having(t.sum_qty_ordered > 3000)
                            #.order_by(desc(t.sum_qty_ordered))

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@bp.route("/report2")
def report2():
    return render_template("report2.jinja")

@bp.route("/report2_data")
def report2_data():
    """ Sales by State table data.
    """

    response_schema = OrderViewSchema(many=True)
    t = OrderView
    dbsession = OrderView.query.session    
    # aggregates defined in model have advantage of sorting by that columns
    query = dbsession.query(t.ship_state,
                            t.sum_qty_ordered,
                            t.sum_price,
                           ).group_by(t.ship_state, t.ship_country)\
                            .having(t.ship_country=='US')

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/report3")
def report3():
    return render_template("report3.jinja")

@bp.route("/report3_data")
def report3_data():
    """ Orders by SKU table data.
    """

    response_schema = OrderViewSchema(many=True)
    t = OrderView
    dbsession = OrderView.query.session    
    # aggregates defined in model have advantage of sorting by that columns
    query = dbsession.query(t.sku,
                            t.markup,
                            t.sum_qty_ordered,
                            t.sum_price,
                           ).group_by(t.sku, t.markup)\
                            .having(t.sum_qty_ordered > 0)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/report4")
def report4():
    return render_template("report4.jinja")

@bp.route("/report4_data")
def report4_data():
    """ Orders by Date table data.
    """

    response_schema = OrderViewSchema(many=True)
    t = OrderView
    dbsession = OrderView.query.session
    # aggregates defined in model have advantage of sorting by that columns
    query = dbsession.query(t.purchase_year,
                            t.purchase_month_name,
                            t.purchase_month,
                            t.sum_qty_ordered,
                            t.sum_price,
                           ).group_by(t.purchase_year, t.purchase_month_name, t.purchase_month)\
                            .having(t.purchase_year>2017)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
