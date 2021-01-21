from marshmallow_sqlalchemy import fields_for_model, auto_field
from api.models.schema_base_classes import (fields,
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
# from api.models.simple_schema import (
#     SalesChannelSchema)
from api.models import combined as m


class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.SalesChannel
        fields = ['description']

class OrdersSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Order
    sales_channel = fields.Nested(SalesChannelSchema)
