from marshmallow_sqlalchemy import fields, auto_field
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from api.models import combined as m


class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.SalesChannel
        fields = ['description']


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Order
        fields = ['order_number', 'purchase_date', 'sales_channel']
    sales_channel = fields.Nested(SalesChannelSchema)


class OrderLinesSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.OrderLine
    promise_date = auto_field(format='%Y-%m-%d')
    order = fields.Nested(OrderSchema)
