# coding: utf-8
from sqlalchemy import event, Column, DateTime, Integer, ForeignKey, String, Boolean, FetchedValue, Unicode
from sqlalchemy.dialects.mssql import VARCHAR
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql import func
from api.models.model_base import db, BIT, Numeric, DECIMAL, DATETIMEOFFSET
from sqlalchemy.ext.hybrid import hybrid_property
from api.models.model_base import NonUnicodeString


class Leader(db.Model):
    __tablename__ = 'Leader'
    __bind_key__ = 'mainDB'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    encrypted_uid = Column(String(50), nullable=False)
    description = Column(String(4000))
    all_pnl = Column(Numeric(18, 2))
    all_roi = Column(Numeric(18, 2))
    is_active = Column(Boolean, nullable=False)


class Trade(db.Model):
    __tablename__ = 'Trade'
    __bind_key__ = 'mainDB'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    change_entry_price = Column(Numeric(18, 6), nullable=False)
    change_size = Column(Numeric(18, 2), nullable=False)
    amount_change = Column(Numeric(18, 2), nullable=False)
    entry_price = Column(Numeric(18, 2), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    position_size = Column(Numeric(18, 2), nullable=False)
    update_time = Column(DateTime)
    leader_id = Column(ForeignKey('Leader.id'), nullable=False)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.now())
    direction = Column(String(50), nullable=False)

    leader = relationship('Leader', backref='trades')

    # expression columns 
    abs_position_size = column_property(
        func.abs(position_size)
    )
    abs_position_amount = column_property(
        func.abs(amount)
    )
    # sum_amount = column_property(
    #     func.sum(amount)
    # )
    # sum_amount_change = column_property(
    #     func.sum(amount_change)
    # )
    # avg_position_size = column_property(
    #     func.avg(position_size)
    # )
    # # count_orders = column_property(
    # #     func.count(distinct(order_id))
    # # )
    # # count_order_lines = column_property(
    # #     func.count(guid_order_line)
    # # )

    @property
    def position_desc(self):
        if self.direction == 'sell-close':
            return "take profit"
        if self.direction == 'buy-close':
            return "take profit - short"
        if self.direction == 'sell' and self.amount >= 0:
            return "take profit"
        if self.direction == 'buy' and self.amount < 0:
            return "take profit - short"
        if self.direction == 'sell' and self.amount < 0:
            return "enter short"
        if self.direction == 'buy' and self.amount >= 0:
            return "enter long"


class KnownPosition(db.Model):
    __tablename__ = 'KnownPosition'
    __bind_key__ = 'mainDB'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    entry_price = Column(Numeric(18, 2), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    position_size = Column(Numeric(18, 2), nullable=False)
    update_time = Column(DateTime)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.now())
    leader_id = Column(ForeignKey('Leader.id'), nullable=False)
    is_active = Column(Boolean, nullable=False,
                       server_default="1")

    leader = relationship('Leader', backref='known_positions')
