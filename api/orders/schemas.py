from api.models.schema_base_classes import (
    SQLAlchemyAutoSchemaOpts,
    fields, SQLAlchemyAutoSchema, SQLAlchemySchema,
    BasicMeta, AliasedFieldsSchema)
from api.models.simple_schema import (
    SalesChannelSchema, OrderLinesSchema, OrdersSchema,
    OrderFlagsSchema, OrderLineFlagsSchema, WarehousesSchema,
    TbProductsSchema)
from api.models import combined as m
from marshmallow_sqlalchemy import fields_for_model, auto_field, field_for, property2field
from marshmallow import pre_load

class OrderFeedsSchema(AliasedFieldsSchema):
    class Meta(BasicMeta):
        model = m.OrderLines
        include_relationships = True
        include_fk = True
        load_instance = True
        # works like this:
        fields = ("order_id",
                  "order.sales_order_number",
                  "order_line_flags.purchase_order_number",
                  "sku",
                  "qty_ordered",
                  "price",
                  "order_line_flags.line_type",
                  "order.purchase_date",
                  "guid_order_line",
                  "order_line_id",
                  "order_line_flags.exported",
                  "order.ship_email",
                  "order.buyer_email",
                  "order.ship_name",
                  "order.ship_address_1",
                  "order.ship_address_2",
                  "order.ship_address_3",
                  "order.ship_city",
                  "order.ship_state",
                  "order.ship_postal_code",
                  "order.ship_country",
                  "order.ship_phone",
                  "order_flags.is_prime",
                  "order_line_flags.is_premium",
                  "order_line_flags.shipping_priority",
                  "order_line_flags.notes",
                  "order_line_flags.promise_date",
                  "order_line_flags.fulfillment_warehouse.abbr",
                  "order_line_flags.fulfillment_warehouse.name",
                  "order_line_flags.OrderLineStatus.description",
                  "product.product_pricing.cost",
                  "product.brand",
                  "product.supplier",
                  "product.upc",
                  "markup",
                  "order.email",
                  'tracking_number',
                  "product.shipping_rules.edi",
                  "product.shipping_rules.leadtime",
                  "order.SalesChannel.description"
                  )
    field_alias_dict = {'order_line_flags.fulfillment_warehouse.abbr': 'fulfillment_warehouse_abbr',
                        'order_line_flags.fulfillment_warehouse.name': 'fulfillment_warehouse_name',
                        'order.SalesChannel.description': 'sales_channel',
                        'order_line_flags.OrderLineStatus.description': 'order_line_status'
                        }
    auto_flatten_fields = True

    order = fields.Nested(OrdersSchema)
    order_line_flags = fields.Nested(OrderLineFlagsSchema)
    product = fields.Nested(TbProductsSchema)
    markup = fields.Method("get_markup")
    #email = fields.Method("get_email")
    #tracking_number = fields.Method("get_tracking_number")

    def get_markup(self, obj):
        if obj.product \
                and obj.product.product_pricing \
                and obj.product.product_pricing.cost > 0 \
                and obj.qty_ordered > 0:
            return int((obj.price / (obj.product.product_pricing.cost * obj.qty_ordered) * 100) - 100)
        else:
            return 0

    # def get_email(self, obj):
    #     if obj.order.ship_email:
    #         return obj.order.ship_email
    #     else:
    #         return obj.order.buyer_email

    def get_tracking_number(self, obj):
        if obj.shipments:
            return obj.shipments.tracking_number
        else:
            return


class UpdateOrderLineFlagsSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = m.OrderLineFlags
        include_relationships = True
        include_fk = True
        load_instance = True
        fields = ('line_type',
                  'qty_shipped',
                  'purchase_order_number',
                  'order_line_status',
                  'exported',
                  'date_exported',
                  'notes',
                  'linked_order_id',
                  'promise_date',
                  'fulfillment_warehouse_id',
                  'is_premium',
                  'shipping_priority')
