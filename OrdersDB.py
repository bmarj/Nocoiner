# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class FulfillmentWarehouse(db.Model):
    __tablename__ = 'fulfillment_warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64, 'Croatian_CI_AS'), nullable=False)
    code = db.Column(db.String(20, 'Croatian_CI_AS'), nullable=False, unique=True)
    enabled = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())



class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Unicode(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    ship_name = db.Column(db.Unicode(500), nullable=False)
    ship_phone = db.Column(db.Unicode(100))
    ship_email = db.Column(db.Unicode(500))
    ship_address = db.Column(db.Unicode(500), nullable=False)
    ship_address_2 = db.Column(db.Unicode(500))
    ship_city = db.Column(db.Unicode(500))
    ship_postal_code = db.Column(db.Unicode(100))
    ship_state = db.Column(db.Unicode(500))
    ship_country = db.Column(db.Unicode(500), nullable=False)
    buyer_name = db.Column(db.Unicode(500))
    buyer_phone = db.Column(db.Unicode(100))
    buyer_email = db.Column(db.Unicode(500))
    buyer_address = db.Column(db.Unicode(500))
    buyer_address_2 = db.Column(db.Unicode(500))
    buyer_city = db.Column(db.Unicode(500))
    buyer_state = db.Column(db.Unicode(500))
    buyer_postal_code = db.Column(db.Unicode(100))
    buyer_country = db.Column(db.Unicode(500))
    sales_channel_id = db.Column(db.ForeignKey('sales_channel.id'), nullable=False)
    created_timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    total_qty = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order_status_id = db.Column(db.ForeignKey('order_status.id'), nullable=False)
    processing_status = db.Column(db.Unicode(20), nullable=False, server_default=db.FetchedValue())
    referring_order = db.Column(db.BigInteger)
    is_prime = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    is_premium = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    shipping_priority = db.Column(db.Unicode(128))

    order_status = db.relationship('OrderStatus', primaryjoin='Order.order_status_id == OrderStatus.id', backref='orders')
    sales_channel = db.relationship('SalesChannel', primaryjoin='Order.sales_channel_id == SalesChannel.id', backref='orders')



class OrderLine(db.Model):
    __tablename__ = 'order_line'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(159, 'Croatian_CI_AS'))
    order_id = db.Column(db.ForeignKey('order.id'), nullable=False, index=True)
    qty_ordered = db.Column(db.Integer, nullable=False)
    qty_shipped = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2))
    currency_code = db.Column(db.Unicode(3), nullable=False)
    shipping_price = db.Column(db.Numeric(10, 2))
    shipping_tax = db.Column(db.Numeric(10, 2))
    line_type = db.Column(db.Unicode(10))
    purchase_order_number = db.Column(db.Unicode(128))
    order_line_status_id = db.Column(db.ForeignKey('order_line_status.id'))
    exported = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    date_exported = db.Column(db.DateTime)
    username = db.Column(db.Unicode(256))
    notes = db.Column(db.Unicode)
    created_date = db.Column(db.DateTime, server_default=db.FetchedValue())
    processed_date = db.Column(db.DateTime)
    promise_date = db.Column(db.DateTime)
    fulfillment_warehouse_id = db.Column(db.ForeignKey('fulfillment_warehouse.id'))
    is_premium = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    shipping_priority = db.Column(db.Unicode(128))

    fulfillment_warehouse = db.relationship('FulfillmentWarehouse', primaryjoin='OrderLine.fulfillment_warehouse_id == FulfillmentWarehouse.id', backref='order_lines')
    order = db.relationship('Order', primaryjoin='OrderLine.order_id == Order.id', backref='order_lines')
    order_line_status = db.relationship('OrderLineStatus', primaryjoin='OrderLine.order_line_status_id == OrderLineStatus.id', backref='order_lines')



class OrderLineStatus(db.Model):
    __tablename__ = 'order_line_status'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20, 'Croatian_CI_AS'), nullable=False, unique=True)
    description = db.Column(db.Unicode(500), nullable=False)



class OrderStatus(db.Model):
    __tablename__ = 'order_status'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Unicode(20), nullable=False, unique=True)
    description = db.Column(db.Unicode(500), nullable=False)



class SalesChannel(db.Model):
    __tablename__ = 'sales_channel'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(100), nullable=False)
    code = db.Column(db.Unicode(20), nullable=False, unique=True)
    service_id = db.Column(db.Unicode(50), unique=True)
    balanceable = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    enabled = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    product_alias_group = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_cross_insert = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())



class ShipServiceLevel(db.Model):
    __tablename__ = 'ship_service_level'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Unicode(20), nullable=False, unique=True)
    description = db.Column(db.Unicode(500))
