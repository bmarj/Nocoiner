from marshmallow_sqlalchemy import fields, fields_for_model, auto_field
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from api import models as m


class LeaderSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Leader
        # fields = ['name', 'encrypted_uid']


class TradesSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Trade
        exclude = ['abs_position_size',
                   'abs_position_amount']
    #position_desc = fields.String()
    leader = fields.Nested(LeaderSchema)


class KnownPositions(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.KnownPosition
    leader = fields.Nested(LeaderSchema)
