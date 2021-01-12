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

class InventoryLinesSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = m.InventoryLocationsAvaiable
        include_relationships = False
        include_fk = False
        load_instance = False

class UpdateInventoryItemSchema(SQLAlchemyAutoSchema):
    class Meta(BasicMeta):
        model = m.TblInvLocations
        include_relationships = True
        include_fk = True
        load_instance = True
        fields = ('lid',
                  'row',
                  'level',
                  'col',
                  'qty',
                  'upc')
