from marshmallow_sqlalchemy import fields, fields_for_model, auto_field
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from api import models as m


class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.SalesChannel
        fields = ['description']


class OrdersSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Order
    sales_channel = fields.Nested(SalesChannelSchema)
