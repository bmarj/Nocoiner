from api.models import (db, Order, OrderLine)
from api.basic_schemas import SalesChannelSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields


class OrderDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
        include_fk = True
        load_instance = True
    sales_channel = fields.Nested(SalesChannelSchema)
    from api.basic_schemas import OrderLineSchema
    order_lines = fields.Nested(OrderLineSchema, many=True)


# class OrderLineSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = OrderLine
#         include_relationships = True
#         include_fk = True
#         load_instance = True
