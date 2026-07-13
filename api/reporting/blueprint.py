from collections import defaultdict
from datetime import timedelta

from flask import Blueprint, session, jsonify, url_for, request, render_template, flash, current_app
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


@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.jinja")

@bp.route("/dashboard_data")
def dashboard_data():
    """Aggregated stats for the overview dashboard.

    Reporting windows end at the newest trade in the database instead of the
    web server's clock.  The collector can be paused (as the current database
    is), and anchoring to ``datetime.now()`` would make a valid snapshot look
    empty.
    """
    as_of = m.Trade.query.with_entities(
        func.max(m.Trade.created_timestamp)
    ).scalar()

    if as_of is None:
        return jsonify(_empty_dashboard_data())

    d90 = as_of - timedelta(days=90)
    d60 = as_of - timedelta(days=60)
    d30 = as_of - timedelta(days=30)
    d24h = as_of - timedelta(hours=24)

    trades = (m.Trade.query
              .join(m.Leader)
              .filter(m.Trade.created_timestamp.between(d90, as_of))
              .order_by(m.Trade.created_timestamp)
              .all())

    daily_pnl = defaultdict(float)
    daily_volume = defaultdict(float)
    daily_count = defaultdict(int)
    daily_wins = defaultdict(int)
    daily_closes = defaultdict(int)
    pnl_by_trader = defaultdict(float)
    volume_by_symbol = defaultdict(float)
    kpi = defaultdict(float)
    traders_30d = set()

    for t in trades:
        ts = t.created_timestamp
        day = ts.date().isoformat()
        volume = abs(t.change_size or 0)
        profit = t.profit

        daily_volume[day] += volume
        daily_count[day] += 1
        volume_by_symbol[t.symbol] += volume
        if profit is not None:
            daily_pnl[day] += profit
            pnl_by_trader[t.leader.name] += profit
            daily_closes[day] += 1
            daily_wins[day] += profit > 0

        if ts >= d30:
            traders_30d.add(t.leader.name)
            kpi['volume_30d'] += volume
            kpi['trades_30d'] += 1
            if ts >= d24h:
                kpi['trades_24h'] += 1
            if profit is not None:
                kpi['pnl_30d'] += profit
                kpi['closes_30d'] += 1
                kpi['wins_30d'] += profit > 0
        elif ts >= d60:
            kpi['volume_prev_30d'] += volume
            kpi['trades_prev_30d'] += 1
            if profit is not None:
                kpi['pnl_prev_30d'] += profit
                kpi['closes_prev_30d'] += 1
                kpi['wins_prev_30d'] += profit > 0

    # cumulative realized P&L over the whole window
    cum_dates, cum_values = [], []
    running = 0.0
    chart_start = as_of.date() - timedelta(days=89)
    for day_offset in range(90):
        day = (chart_start + timedelta(days=day_offset)).isoformat()
        running += daily_pnl.get(day, 0)
        cum_dates.append(day)
        cum_values.append(round(running, 2))

    # 14-day sparklines, zero-filled so quiet days show as flat
    spark_start = as_of.date() - timedelta(days=13)
    spark_days = [(spark_start + timedelta(days=i)).isoformat()
                  for i in range(14)]
    winrate_spark, cum_wins, cum_closes = [], 0, 0
    for d in spark_days:
        cum_wins += daily_wins.get(d, 0)
        cum_closes += daily_closes.get(d, 0)
        winrate_spark.append(round(100.0 * cum_wins / cum_closes, 1)
                             if cum_closes else 0)
    sparks = {
        'pnl': [round(daily_pnl.get(d, 0), 2) for d in spark_days],
        'volume': [round(daily_volume.get(d, 0), 2) for d in spark_days],
        'trades': [daily_count.get(d, 0) for d in spark_days],
        'winrate': winrate_spark,
    }

    by_trader = sorted(({'name': n, 'pnl': round(v, 2)}
                        for n, v in pnl_by_trader.items()),
                       key=lambda r: r['pnl'], reverse=True)

    symbols_ranked = sorted(volume_by_symbol.items(),
                            key=lambda kv: kv[1], reverse=True)
    by_symbol = [{'symbol': s, 'volume': round(v, 2)}
                 for s, v in symbols_ranked[:7]]
    tail = sum(v for _, v in symbols_ranked[7:])
    if tail:
        by_symbol.append({'symbol': 'Other', 'volume': round(tail, 2)})

    recent = [{
        'symbol': t.symbol,
        'desc': t.position_desc,
        'is_long': (t.amount or 0) >= 0 and t.direction != 'buy-close',
        'change_size': round(t.change_size or 0, 2),
        'profit': round(t.profit, 2) if t.profit is not None else None,
        'trader': t.leader.name,
        'time': t.created_timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
    } for t in trades[-8:][::-1]]

    active_traders = (m.Leader.query
                      .filter(m.Leader.is_active)
                      .count())
    open_positions = (m.KnownPosition.query
                      .filter(m.KnownPosition.is_active)
                      .count())

    win_rate = (100.0 * kpi['wins_30d'] / kpi['closes_30d']) if kpi['closes_30d'] else 0
    win_rate_prev = (100.0 * kpi['wins_prev_30d'] / kpi['closes_prev_30d']) if kpi['closes_prev_30d'] else 0

    return jsonify({
        'meta': {
            'as_of': as_of.strftime('%Y-%m-%dT%H:%M:%S'),
            'window_start': d90.strftime('%Y-%m-%dT%H:%M:%S'),
            'has_data': True,
        },
        'kpis': {
            'pnl_30d': round(kpi['pnl_30d'], 2),
            'pnl_delta': round(kpi['pnl_30d'] - kpi['pnl_prev_30d'], 2),
            'volume_30d': round(kpi['volume_30d'], 2),
            'volume_delta': round(kpi['volume_30d'] - kpi['volume_prev_30d'], 2),
            'trades_30d': int(kpi['trades_30d']),
            'trades_24h': int(kpi['trades_24h']),
            'win_rate_30d': round(win_rate, 1),
            'win_rate_delta': round(win_rate - win_rate_prev, 1),
            'closes_30d': int(kpi['closes_30d']),
            'active_traders': active_traders,
            'traders_30d': len(traders_30d),
            'open_positions': open_positions,
        },
        'cum_pnl': {'dates': cum_dates, 'values': cum_values},
        'sparks': {'days': spark_days, **sparks},
        'by_trader': by_trader,
        'by_symbol': by_symbol,
        'recent': recent,
    })


def _empty_dashboard_data():
    """Return the dashboard response shape when the database has no trades."""
    return {
        'meta': {'as_of': None, 'window_start': None, 'has_data': False},
        'kpis': {
            'pnl_30d': 0,
            'pnl_delta': 0,
            'volume_30d': 0,
            'volume_delta': 0,
            'trades_30d': 0,
            'trades_24h': 0,
            'win_rate_30d': 0,
            'win_rate_delta': 0,
            'closes_30d': 0,
            'active_traders': 0,
            'traders_30d': 0,
            'open_positions': 0,
        },
        'cum_pnl': {'dates': [], 'values': []},
        'sparks': {
            'days': [], 'pnl': [], 'volume': [], 'trades': [], 'winrate': []
        },
        'by_trader': [],
        'by_symbol': [],
        'recent': [],
    }
