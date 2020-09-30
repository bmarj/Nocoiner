from api.schema_base_classes import (
    fields, SQLAlchemyAutoSchema,
    BasicMeta, Reach)
from api.simple_schema import (
    SalesChannelSchema, OrderLineSchema, OrderSchema)
from api.models import (Order, OrderLine)


class OrderDetailSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = Order
        include_relationships = True
        include_fk = True
        load_instance = True
    sales_channel = fields.Nested(SalesChannelSchema)
    order_lines = fields.Nested(OrderLineSchema, many=True)


class OrderFeedsSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = OrderLine
        include_relationships = True
        include_fk = True
        load_instance = True
        # works like this:
        # fields = ('line_type','sku','shipping_price', 'order.order_id') 
    # order_id = Reach(fields.Str(), data_key="order", path="address.street")
    # order = fields.Nested(OrderSchema)
    # order_id = Reach(fields.Str(), data_key="order_id", path="order.order_id")
    # order_id = ma.Pluck(OrderSchema, 'order_id')
    # order_id = fields.Str()
