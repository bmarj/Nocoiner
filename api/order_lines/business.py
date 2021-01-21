from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from api.models import OrderLine, OrderLineStatus, Order, SalesChannel
from api.models.model_base import db, filter_query, sort_query, paginate_query, get_model_changes
#from .schemas import UpdateInventoryItemSchema

def get_order_lines():
    # join to eager load relations
    q = OrderLine.query\
        .join(Order)\
        .outerjoin(SalesChannel)
    return q

def get_order_line_by_id(object_id):
    q = OrderLine.query\
        .filter(OrderLine.id == object_id)\
        .first()
    return q

def set_order_line_status(order, status_text):
    q = OrderLineStatus.query\
        .filter(OrderLineStatus.code == status_text)\
        .first()
    order.OrderStatus = q
