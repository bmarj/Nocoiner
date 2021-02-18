# coding: utf-8
from sqlalchemy import event, Column, DateTime, Integer, ForeignKey, String, Boolean, FetchedValue, Unicode
from sqlalchemy.dialects.mssql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.models.model_base import db, BIT, Numeric, DECIMAL, DATETIMEOFFSET
from sqlalchemy.ext.hybrid import hybrid_property
from api.models.model_base import NonUnicodeString

class FulfillmentWarehouse(db.Model):
    __tablename__ = 'fulfillment_warehouse'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    name                = Column(String(64), nullable=False)
    code                = Column(String(20), nullable=False, unique=True)
    enabled             = Column(Boolean, nullable=False, server_default="1")


class Order(db.Model):
    __tablename__ = 'order'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    order_number        = Column(Unicode(50), nullable=False)
    purchase_date       = Column(DateTime, nullable=False)
    ship_name           = Column(Unicode(500), nullable=False)
    ship_phone          = Column(Unicode(100))
    ship_email          = Column(Unicode(500))
    ship_address        = Column(Unicode(500), nullable=False)
    ship_address_2      = Column(Unicode(500))
    ship_city           = Column(Unicode(500))
    ship_postal_code    = Column(Unicode(100))
    ship_state          = Column(Unicode(500))
    ship_country        = Column(Unicode(500), nullable=False)
    buyer_name          = Column(Unicode(500))
    buyer_phone         = Column(Unicode(100))
    buyer_email         = Column(Unicode(500))
    buyer_address       = Column(Unicode(500))
    buyer_address_2     = Column(Unicode(500))
    buyer_city          = Column(Unicode(500))
    buyer_state         = Column(Unicode(500))
    buyer_postal_code   = Column(Unicode(100))
    buyer_country       = Column(Unicode(500))
    sales_channel_id    = Column(ForeignKey('sales_channel.id'), nullable=False)
    created_timestamp   = Column(DateTime, nullable=False, server_default=func.now())
    total_qty           = Column(Integer, nullable=False, server_default="0")
    order_status_id     = Column(ForeignKey('order_status.id'), nullable=False)
    processing_status   = Column(Unicode(20), nullable=False, server_default='Pending')
    referring_order     = Column(Integer)
    is_prime            = Column(Boolean, nullable=False, server_default="0")
    is_premium          = Column(Boolean, nullable=False, server_default="0")
    shipping_priority   = Column(Unicode(128))

    order_status        = relationship('OrderStatus',
                                       foreign_keys=order_status_id,
                                       backref='orders')
    sales_channel       = relationship('SalesChannel',
                                       foreign_keys=sales_channel_id,
                                       backref='orders')


class OrderLine(db.Model):
    __tablename__ = 'order_line'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    sku                 = Column(NonUnicodeString(159))
    order_id            = Column(ForeignKey('order.id'), nullable=False)
    qty_ordered         = Column(Integer, nullable=False)
    qty_shipped         = Column(Integer, nullable=False,
                                 server_default="0")
    price               = Column(Numeric(10, 2), nullable=False)
    tax                 = Column(Numeric(10, 2))
    currency_code       = Column(Unicode(3), nullable=False)
    shipping_price      = Column(Numeric(10, 2))
    shipping_tax        = Column(Numeric(10, 2))
    line_type           = Column(Unicode(10))
    purchase_order_number \
                        = Column(Unicode(128))
    order_line_status_id \
                        = Column(ForeignKey('order_line_status.id'))
    exported            = Column(Boolean, nullable=False,
                                 server_default="0")
    date_exported       = Column(DateTime)
    username            = Column(Unicode(256))
    notes               = Column(Unicode)
    created_date        = Column(DateTime, server_default=func.now())
    processed_date      = Column(DateTime)
    promise_date        = Column(DateTime)
    fulfillment_warehouse_id \
                        = Column(ForeignKey('fulfillment_warehouse.id'))
    is_premium          = Column(Boolean, nullable=False,
                                 server_default="0")
    shipping_priority   = Column(Unicode(128))

    fulfillment_warehouse = relationship('FulfillmentWarehouse',
                                         foreign_keys=fulfillment_warehouse_id,
                                         backref='order_lines')
    order               = relationship('Order',
                                       foreign_keys=order_id,
                                       backref='order_lines')
    order_line_status   = relationship('OrderLineStatus',
                                       foreign_keys=order_line_status_id,
                                       backref='order_lines')


class OrderLineStatus(db.Model):
    __tablename__ = 'order_line_status'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    code                = Column(String(20), nullable=False, unique=True)
    description         = Column(Unicode(500), nullable=False)


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    code                = Column(Unicode(20), nullable=False, unique=True)
    description         = Column(Unicode(500), nullable=False)


class SalesChannel(db.Model):
    __tablename__ = 'sales_channel'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    description         = Column(Unicode(100), nullable=False)
    code                = Column(Unicode(20), nullable=False, unique=True)
    service_id          = Column(Unicode(50), unique=True)
    balanceable         = Column(Boolean, nullable=False,
                                 server_default="0")
    enabled             = Column(Boolean, nullable=False,
                                 server_default="1")
    product_alias_group = Column(Integer, nullable=False,
                                 server_default="0")
    is_cross_insert     = Column(Boolean, nullable=False,
                                 server_default="0")


class ShipServiceLevel(db.Model):
    __tablename__ = 'ship_service_level'
    __bind_key__ = 'ordersDB'

    id                  = Column(Integer, primary_key=True)
    code                = Column(Unicode(20), nullable=False, unique=True)
    description         = Column(Unicode(500))
