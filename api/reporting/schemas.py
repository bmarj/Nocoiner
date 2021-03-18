from marshmallow_sqlalchemy import fields_for_model, auto_field
from marshmallow import fields
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from api.models import combined as m
from . import model as r


class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.SalesChannel
        fields = ['description']

class OrderViewSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = r.OrderView
    # sales_channel = fields.Nested(SalesChannelSchema)

    # redefine data type for expression columns in model
    sum_qty_shipped = fields.Int()
    sum_qty_ordered = fields.Int()
    sum_price = fields.Number()
    sum_line_cost = fields.Number()
    count_orders = fields.Int()
    count_order_lines = fields.Int()

class InventoryViewSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = r.InventoryView
