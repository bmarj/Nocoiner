import datetime
import json
from flask import request, session, jsonify
#from lxml import etree

# from commerceblitz_api.models import orders_model
from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from api.models.combined import OrderLines, OrderLineFlags, Orders, OrderFlags, Warehouses, OrderLineFlagsLog
from api.models.model_base import db, filter_query, sort_query, paginate_query, get_model_changes
from .schemas import OrderFeedsSchema, UpdateOrderLineFlagsSchema

def order_lines_query():

    # q = db.session.query(OrderLines)\
    #     .options(joinedload(OrderLines.shipments),
    #              joinedload(OrderLines.order),
    #              joinedload(OrderLines.order_line_flags),
    #              joinedload(OrderLines.product),
    #              raiseload("*"))

    # q = db.session.query(OrderLines)

    # q = db.session.query(OrderLines)\
    #     .options(
    #         orm.joinedload(OrderLines.order_line_flags))

    q = db.session.query(OrderLines)\
        .join(OrderLineFlags)

    # q = db.session.query(OrderLines)\
    #     .options(joinedload(OrderLines.shipments))\
    #     .options(joinedload(OrderLines.order))\
    #     .options(joinedload(OrderLines.order_line_flags))\
    #     .options(joinedload(OrderLines.product))
    #     .options(
    #         joinedload(OrderLines.order)
    #         #.joinedload(OrderLines.order_line_flags)
    #         #.joinedload(OrderLines.product)
    #         .joinedload(Orders.order_flags)
    #         #.joinedload(OrderLineFlags.fulfillment_warehouse)
    # ).options(
    #         #.joinedload(OrderLines.product)
    #         joinedload(OrderLines.order_line_flags)
    #         .joinedload(OrderLineFlags.fulfillment_warehouse)
    # )
    #.options(contains_eager(OrderLines.order))
    # .join(Orders)\
    # .outerjoin(OrderFlags)\
    # .outerjoin(OrderLineFlags)\
    # .outerjoin(Warehouses)

    return q


def get_order_lines(filtering, sorting, paging):

    q = OrderLines.query\
        .join(Orders)\
        .outerjoin(OrderFlags)\
        .outerjoin(OrderLineFlags)\
        .outerjoin(Warehouses)

    q = filter_query(q, filtering)
    q = sort_query(q, sorting)

    return paginate_query(q, paging)

def update_order_line_flags(update_object):

    input_schema = UpdateOrderLineFlagsSchema()
    for object_id, update_cols in update_object.items():
        # fetch object from db
        update_obj = OrderLineFlags.query.get_or_404(object_id)
        input_data = {item["column"]: item["value"] for item in update_cols}
        # update object with values
        oo = input_schema.load(input_data, instance=update_obj, partial=True, unknown=EXCLUDE)
        changes = get_model_changes(update_obj, "guid_order_line")
        for change in changes:
            log_obj = OrderLineFlagsLog(**change, user=session["username"], timestamp=datetime.datetime.now())
            db.session.add(log_obj)

    # commit to db
    db.session.commit()

    return len(update_object)
