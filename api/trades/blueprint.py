from flask import Blueprint, session, jsonify, url_for, request, render_template, flash
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
import requests
# from marshmallow.exceptions import ValidationError

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import generic_add, generic_edit, generic_form_edit, generic_add
from api.models.binance_leader_trades import Leader
from .business import query_active_positions, query_traders, query_trades
from .schemas import (
    KnownPositions,
    LeaderSchema,
    TradesSchema)
from .forms import LeaderForm, TradeForm
from .binance_leaderboard import process_leaders_data

bp = Blueprint('trades', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')

@bp.route("/trades")
# @authorize('trades')
def trades_view():
    trader_id = request.values.get("trader_id")
    return render_template("trades.jinja", trader_id=trader_id)

@bp.route("/trades_data")
# @authorize('trades')
def trades_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_trades()
    response_schema = TradesSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/positions")
# @authorize('trades')
def positions_view():
    trader_id = request.values.get("trader_id")
    return render_template("positions.jinja", trader_id=trader_id)

@bp.route("/positions_data")
# @authorize('trades')
def positions_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_active_positions()
    response_schema = KnownPositions(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/traders")
# @authorize('trades')
def traders_view():
    return render_template("traders.jinja")

@bp.route("/traders_data")
# @authorize('trades')
def traders_data():

    """Return server side data."""
    # defining the initial query depending on your purpose
    query = query_traders()
    response_schema = LeaderSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@bp.route("/process_traders", methods=['GET'])
def process_traders():
    process_leaders_data()
    return "OK"

@bp.route("/process_leaders/<id>", methods=['POST'])
# @authorize('trades')
def process_leaders(id):
    process_leaders_data()
    return render_template("form_success.jinja")

# generic editing
# need to change only permited forms
# Use with 'edit_button' button
# Used for editing with all permited_forms withing blueprint
@bp.route('/form_edit/<id>', methods=['GET'])
@bp.route('/form_edit', methods=['GET','POST'])
# @authorize('trades')
def form_edit(id=None):
    permitted_forms = [LeaderForm]
    return generic_form_edit(url_for('.form_edit'), permitted_forms, id)

# editing with dedicated endpoint and form
# Use with 'edit' button
@bp.route('/leader_edit/<id>', methods=['GET'])
@bp.route('/leader_edit', methods=['GET', 'POST'])
@authorize('trades')
def leader_edit(id=None):
    return generic_edit(LeaderForm, 'leader_add.jinja', url_for('.leader_edit'), id)

@bp.route('/leader_add', methods=['GET', 'POST'])
@authorize('trades')
def leader_add():
    return generic_add(LeaderForm, 'leader_add.jinja', url_for('.leader_add'))
