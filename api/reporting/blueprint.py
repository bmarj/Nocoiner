from flask import Blueprint, session, jsonify, url_for, request, render_template, flash, current_app
from flask_sqlalchemy import orm
from marshmallow import EXCLUDE
# from marshmallow.exceptions import ValidationError
from sqlalchemy.sql import select, desc, or_, and_
from sqlalchemy.orm import object_session
from sqlalchemy import func, bindparam

from api.datatables import DataTables
from api.user_management import login_required, authorize
from api.utils.common import generic_edit, generic_form_edit, generic_form_delete
from api.models import binance_leader_trades as m
from . import model as r
from .schemas import (
    TradeSchema,
    TradeAgregatedSchema,
    PositionSchema)
# from .forms import OrderForm

bp = Blueprint('reporting', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/reporting/static')


@bp.route("/transactions")
def transactions():
    return render_template("transactions.jinja")

@bp.route("/transactions_data")
def transactions_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = (m.Trade.query
              .join(m.Leader))
    response_schema = TradeSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@bp.route("/tradeactivity")
def tradeactivity():
    return render_template("tradeactivity.jinja")

@bp.route("/tradeactivity_data")
def tradeactivity_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    t = m.KnownPosition
    dbsession = t.query.session
    response_schema = PositionSchema(many=True)

    # aggregates defined in query work this way
    query = dbsession.query(t.symbol, t.leader_id,
                            func.count(t.id).label('number_of_trades')
                            ).join(m.Leader).group_by(t.symbol, t.leader_id)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())

@bp.route("/tradedvalue")
def tradedvalue():
    return render_template("tradedvalue.jinja")

@bp.route("/tradedvalue_data")
def tradedvalue_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    t = r.TradeAgregated
    dbsession = t.query.session
    response_schema = TradeAgregatedSchema(many=True)

    # aggregates defined in model have advantage of sorting by that columns
    # select columns from model
    query = dbsession.query(t.symbol, t.leader,
                            t.avg_position_size,
                            t.sum_amount,
                            t.sum_amount_change,
                            t.sum_abs_change_size,
                            t.avg_abs_position_size,
                            t.sum_abs_amount,
                            t.sum_abs_amount_change,
                            t.avg_entry_price
                            ).group_by(t.symbol, t.leader)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


@bp.route("/profitloss")
def profitloss():
    return render_template("profitloss.jinja")

@bp.route("/profitloss_data")
def profitloss_data():
    """Return server side data."""
    # defining the initial query depending on your purpose
    query = (m.Trade.query
              .join(m.Leader)
              .filter(or_(m.Trade.direction in ('sell-close', 'buy-close'),
                          and_(m.Trade.direction == 'buy', m.Trade.amount < 0),
                          and_(m.Trade.direction == 'sell', m.Trade.amount >= 0)
                          ))
             )
    response_schema = TradeSchema(many=True)

    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(request.args, query, response_schema)
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())


# import openai
# openai.api_key = current_app.config['OPENAI_API_KEY']
# openai.api_base = current_app.config['OPENAI_BASE_ADDRESS']
# @bp.route("/forinrobot")
# def robot():
#     # List Engines (Models)
#     engines = openai.Engine.list()
#     # Print all engines IDs
#     for engine in engines.data:
#         print(engine.id)

#     # Create a completion, return results streaming as they are generated. Run with `python3 -u` to ensure unbuffered output.
#     completion = openai.Completion.create(
#         engine="gpt-j-6b",
#         prompt="Once upon a time there was a Goose. ",
#         max_tokens=160,
#         stream=True)

#     # Print each token as it is returned
#     for c in completion:
#         print(c.choices[0].text, end='')

#     print("")
