from api.models import (
    db,
    Order, OrderLine,
    OrderStatus, OrderLineStatus,
    SalesChannel, ShipServiceLevel,
    FulfillmentWarehouse)
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

class SimpleMeta:
    """
    Simple table schema rules
    """
    include_relationships = False
    include_fk = False
    load_instance = True

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
