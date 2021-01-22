from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from api.models import Order, OrderStatus, SalesChannel
from api.models.model_base import db, filter_query, sort_query, paginate_query, get_model_changes
#from .schemas import UpdateInventoryItemSchema

###
### Queries (to enable further server side processing like sorting, paging and filtering)
###
def query_orders():
    # join to eager load relations
    q = Order.query\
        .outerjoin(SalesChannel)
    return q

###
### Fetch or process objects
###
def get_order_by_id(object_id):
    q = Order.query\
        .filter(Order.id == object_id)\
        .first()
    return q

def set_order_status(order, status_text):
    q = OrderStatus.query\
        .filter(OrderStatus.code == status_text)\
        .first()
    order.OrderStatus = q
