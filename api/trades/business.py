from typing import List
from sqlalchemy.sql.elements import not_
from api.trades.schemas import KnownPositions
from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from sqlalchemy.sql.expression import true
from api.models import Trade, KnownPosition, Leader
from api.models.model_base import (db, filter_query, sort_query, paginate_query, get_model_changes)


###
### Queries (to enable further server side processing like sorting, paging and filtering)
###
def query_trades():
    # join to eager load relations
    q = Trade.query\
        .join(Leader)
    return q

def query_trader_positions(trader_id=None):
    # join to eager load relations
    q = KnownPosition.query
    if trader_id:
        q = q.filter(KnownPositions.leader.id == trader_id)
    return q

def query_active_positions(trader_id=None):
    # join to eager load relations
    q = KnownPosition.query\
        .join(Leader)\
        .filter(KnownPosition.is_active)
    if trader_id:
        q = q.filter(KnownPositions.leader.id == trader_id)
    return q

def query_traders():
    # join to eager load relations
    q = Leader.query
    return q

###
### Fetch or process objects
###
def get_trade_by_id(object_id):
    q = Trade.query\
        .filter(Trade.id == object_id)\
        .first()
    return q


def get_positions(symbols: List[str], leader_id: int):
    # join to eager load relations
    q = KnownPosition.query\
        .join(Leader)\
        .filter(KnownPosition.is_active,
                KnownPosition.leader_id == leader_id,
                KnownPosition.symbol.in_(symbols))\
        .all()
    return q


def get_positions_except(symbols: List[str], leader_id: int):
    # join to eager load relations
    q = KnownPosition.query\
        .filter(KnownPosition.is_active,
                KnownPosition.leader_id == leader_id,
                not_(KnownPosition.symbol.in_(symbols)))\
        .all()
    return q


def deactivate_positions(symbols: List[str], leader_id: int):
    # join to eager load relations
    q = KnownPosition.query\
        .filter(KnownPosition.is_active,
                KnownPosition.leader_id == leader_id,
                KnownPosition.symbol.in_(symbols))\
        .all()

    for pos in q:
        pos.is_active = False

    return q

def save_position(position: KnownPosition):
    deactivate_positions([position.symbol], position.leader_id)
    newpos = KnownPosition()
    position.is_active = True
    db.session.add(position)

def save_trade(trade: Trade):
    db.session.add(trade)

def get_leaders():
    q = Leader.query\
        .all()
    return q
