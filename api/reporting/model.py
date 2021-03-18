# coding: utf-8
from sqlalchemy import event, Column, DateTime, Integer, ForeignKey, String, Boolean, FetchedValue, Unicode
from sqlalchemy import select, func
from sqlalchemy.dialects.mssql import VARCHAR
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import distinct
from api.models.model_base import db, BIT, Numeric, DATETIMEOFFSET, NonUnicodeString


class OrderView(db.Model):
    __tablename__ = 'materialized_order_view'
    __bind_key__ = 'reportDB'

    guid_order_line = Column(Unicode(40), primary_key=True)
    order_id = Column(Unicode(100))
    purchase_date = Column(DateTime)
    ship_name = Column(Unicode(500))
    ship_city = Column(Unicode(500))
    ship_state = Column(Unicode(500))
    ship_postal_code = Column(Unicode(100))
    ship_country = Column(Unicode(500))
    sales_order_number = Column(Integer)
    sales_channel = Column(Integer)
    order_status = Column(Integer)
    processing_status = Column(Integer)
    shipping_priority_order = Column(Unicode(128))
    qty_ordered = Column(Integer)
    qty_shipped = Column(Integer)
    price = Column(Numeric(18,2))
    tax = Column(Numeric(18,2))
    shipping_price = Column(Numeric(18,2))
    shipping_tax = Column(Numeric(18,2))
    sku = Column(Unicode(128))
    line_type = Column(Unicode(10))
    processed_date = Column(DateTime)
    purchase_order_number = Column(Unicode(128))
    order_line_status = Column(Unicode(10))
    exported = Column(BIT)
    username = Column(Unicode(256))
    linked_order_id = Column(Unicode(128))
    promise_date = Column(DateTime)
    fulfillment_warehouse_id = Column(Integer)
    is_premium_order_line = Column(BIT)
    shipping_priority_order_line = Column(Unicode(128))
    tracking_number = Column(Unicode(128))
    brand = Column(Unicode(128))
    line_cost = Column(Numeric(18,2))
    markup = Column(Integer)
    purchase_year = Column(Integer)
    purchase_month = Column(Integer)
    purchase_month_name = Column(Unicode(128))
    purchase_year_month = Column(DateTime)
    purchase_year_month_day = Column(DateTime)

    # expression columns 
    sum_qty_ordered = column_property(
        func.sum(qty_ordered)
    )
    sum_qty_shipped = column_property(
        func.sum(qty_shipped)
    )
    sum_price = column_property(
        func.sum(price)
    )
    sum_line_cost = column_property(
        func.sum(line_cost)
    )
    count_orders = column_property(
        func.count(distinct(order_id))
    )
    count_order_lines = column_property(
        func.count(guid_order_line)
    )
    # SalesChannel = relationship('SalesChannel',
    #                               primaryjoin='foreign(OrderView.sales_channel) == remote(SalesChannel.sales_channel)')

class InventoryView(db.Model):
    __tablename__ = 'materialized_inventory'
    __bind_key__ = 'reportDB'

    lid = Column(Integer, primary_key=True)
    col = Column(Unicode(10))
    row = Column(Unicode(10))
    level = Column(Unicode(10))
    qty = Column(Integer)
    lastmodtime = Column(DateTime)
    available_qty = Column(Integer)
    upc = Column(Unicode(25))
    sku = Column(Unicode(128))
    brand = Column(Unicode(64))
    supplier = Column(Unicode(64))
    gender = Column(Unicode(64))
    product_name = Column(Unicode(128))
    product_type = Column(Unicode(16))
    price = Column(Numeric(18,2))
    cost = Column(Numeric(18,2))


# class SalesChannel(db.Model):
#     __tablename__ = 'sales_channel'
#     __bind_key__ = 'reportDB'

#     sales_channel = Column(Integer, primary_key=True)
#     description = Column(Unicode(100), unique=True)
#     abbr = Column(Unicode(10), unique=True)
#     service_id = Column(Unicode(50), unique=True)
#     balanceable = Column(BIT)
#     enabled = Column(BIT)
#     product_alias_group = Column(Integer)
#     is_cross_insert = Column(BIT)



# class Warehouses(db.Model):
#     __tablename__ = 'warehouses'
#     __bind_key__ = 'reportDB'

#     warehouse_id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     abbr = Column(String(10))
#     enabled = Column(BIT)


# class ZipCodes(db.Model):
#     __tablename__ = 'zip_codes'
#     __bind_key__ = 'ordersDB'

#     zip_code = Column(String(25))
#     state = Column(String(5))
#     id = Column(Integer, primary_key=True)
