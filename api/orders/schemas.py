from api.schema_base_classes import (
    fields, SQLAlchemyAutoSchema, SQLAlchemySchema,
    BasicMeta, AliasedFieldsSchema)
from api.simple_schema import (
    SalesChannelSchema, OrderLineSchema, OrderSchema)
from api.models import (Order, OrderLine)
from marshmallow_sqlalchemy import fields_for_model, auto_field, field_for, property2field


class OrderDetailSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = Order
        include_relationships = True
        include_fk = True
        load_instance = True
    sales_channel = fields.Nested(SalesChannelSchema)
    order_lines = fields.Nested(OrderLineSchema, many=True)


class OrderFeedsSchema(AliasedFieldsSchema):
    class Meta(BasicMeta):
        model = OrderLine
        include_relationships = True
        include_fk = True
        load_instance = True
        # works like this:
        fields = ("created_date", "currency_code", "date_exported", "exported",
                  "fulfillment_warehouse", "id", "id_fulfillment_warehouse",
                  "id_order", "id_order_line_status", "is_premium",
                  "line_type", "notes", "order.buyer_address",
                  "order.buyer_address_2", "order.buyer_city",
                  "order.buyer_country", "order.buyer_email",
                  "order.buyer_name", "order.buyer_phone",
                  "order.buyer_postal_code", "order.buyer_state",
                  "order.created_timestamp",  # "order.is_premium",
                  "order.is_prime", "order.order_id",
                  "order.processing_status", "order.purchase_date",
                  "order.referring_order", "order.ship_address",
                  "order.ship_address_2", "order.ship_city",
                  "order.ship_country", "order.ship_email", "order.ship_name",
                  "order.ship_phone", "order.ship_postal_code",
                  "order.ship_state", "order.total_qty", "order_line_status",
                  "price", "processed_date", "promise_date",
                  "purchase_order_number", "qty_ordered", "qty_shipped",
                  "shipping_price", "shipping_priority", "shipping_tax", "sku",
                  "tax", "username")
    field_alias_dict = {'order.ship_address': 'ship_address_1',
                        'purchase_order_number': 'sales_order_number',
                        'order.buyer_name': 'buyer_name'}
    auto_flatten_fields = True


    #fields = ('line_type','sku','shipping_price', 'order.order_id')
    #fields = ('line_type','sku','shipping_price', 'qty_ordered', 'username', 'promise_date')
    # order_id = Reach(fields.Str(), data_key="order", path="address.street")
    # order = fields.Nested(OrderSchema)
    # order_id = Reach(fields.Str(), data_key="order_id", path="order.order_id")
    # order_id = ma.Pluck(OrderSchema, 'order_id')
    # order_id = fields.Str()
    # order_id = order.__dict__.get("order_id")
    # order_id = field_for(Order, "order_id")
    # order_id = auto_field("order_id", model = Order)
    # order_id = auto_field("order_id", model=Order)
