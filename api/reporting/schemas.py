from marshmallow_sqlalchemy import fields_for_model, auto_field
from marshmallow import fields
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from api.models import binance_leader_trades as m
from . import model as r

class LeaderSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Leader


class TradeSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Trade
        exclude = []
                #    'sum_amount',
                #    'sum_amount_change',
                #    'avg_position_size']
    leader = fields.Nested(LeaderSchema)

    # redefine data type for expression columns in model
    abs_position_size = fields.Number()
    abs_position_amount = fields.Number()
    # sum_amount = fields.Number()
    # sum_amount_change = fields.Number()
    # avg_position_size = fields.Number()
    position_desc = fields.String()
    profit = fields.Number()


class TradeAgregatedSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = r.TradeAgregated
        exclude = []
                #    'sum_amount',
                #    'sum_amount_change',
                #    'avg_position_size']
    # trader = fields.String(default=None, attribute='leader')

    leader = fields.String()
    # redefine data type for expression columns in model
    abs_position_size = fields.Number()
    abs_position_amount = fields.Number()
    abs_change_size = fields.Number()
    sum_abs_change_size = fields.Number()
    sum_amount = fields.Number()
    sum_amount_change = fields.Number()
    avg_position_size = fields.Number()
    sum_abs_amount = fields.Number()
    sum_abs_amount_change = fields.Number()
    sum_abs_position_size = fields.Number()
    avg_abs_position_size = fields.Number()
    avg_entry_price  = fields.Number()
    description = fields.String()


class PositionSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.KnownPosition

class PositionSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.KnownPosition
        #only = ['id']
    id = auto_field()
    symbol = auto_field()
    leader_id = auto_field()
    number_of_trades = fields.Int()
    # trader = fields.String(attribute='leader.name')

    # tradername = fields.Nested(LeaderSchema, only=['name'])

