from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from api.models import OrderLines, OrderStatus, SalesChannel, Orders
from api.models.model_base import db, filter_query, sort_query, paginate_query, get_model_changes
#from .schemas import UpdateInventoryItemSchema

###
### Queries (to enable further server side processing like sorting, paging and filtering)
###
def query_order_lines():
    # join to eager load relations
    q = OrderLines.query\
        .join(Orders, Orders.order_id == OrderLines.order_id)
        #.outerjoin(SalesChannel.sales_channel == Orders.sales_channel)
    return q

###
### Fetch or process objects
###
