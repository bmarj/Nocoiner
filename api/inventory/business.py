import datetime
import json
from flask import request, session, jsonify
#from lxml import etree

# from commerceblitz_api.models import orders_model
from sqlalchemy.sql import func, join
from flask_sqlalchemy import orm
# import contains_eager, joinedload, subquery, raiseload
from marshmallow import EXCLUDE
from api.models.combined import InventoryLocationsAvaiable, InventoryLocationsSpecial, TblInvLocations, ScanLogWorkingLocations
from api.models.model_base import db, filter_query, sort_query, paginate_query, get_model_changes
from .schemas import UpdateInventoryItemSchema

def inventory_lines():

    q = InventoryLocationsAvaiable.query

    return q

def get_inventory_line_by_id(object_id):

    q = TblInvLocations.query\
        .filter(TblInvLocations.lID == object_id)\
        .first()

    return q


# def update_order_line_flags(update_object):

#     input_schema = UpdateInventoryItemSchema()
#     for object_id, update_cols in update_object.items():
#         # fetch object from db
#         update_obj = TblInvLocations.query.get_or_404(object_id)
#         input_data = {item["column"]: item["value"] for item in update_cols}
#         # update object with values
#         oo = input_schema.load(input_data, instance=update_obj, partial=True, unknown=EXCLUDE)
#         changes = get_model_changes(update_obj, "guid_order_line")
#         for change in changes:
#             log_obj = OrderLineFlagsLog(**change, user=session["username"], timestamp=datetime.datetime.now())
#             db.session.add(log_obj)

#     # commit to db
#     db.session.commit()

#     return len(update_object)
