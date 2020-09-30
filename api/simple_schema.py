from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from api.models import (
    Order, OrderLine,
    OrderStatus, OrderLineStatus,
    SalesChannel, ShipServiceLevel,
    FulfillmentWarehouse)
from api.schema_base_classes import SimpleMeta

ma = Marshmallow()


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = Order


class OrderLineSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = OrderLine


class OrderStatusSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = OrderStatus


class OrderLineStatusSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = OrderLineStatus


class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = SalesChannel


class ShipServiceLevelSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = ShipServiceLevel


class FulfillmentWarehouseSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = FulfillmentWarehouse
