# coding: utf-8
from sqlalchemy import event, Column, DateTime, Integer, ForeignKey, String, Boolean, FetchedValue, Unicode
from sqlalchemy.dialects.mssql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.models.model_base import db, BIT, Numeric, DATETIMEOFFSET
from sqlalchemy.ext.hybrid import hybrid_property
from api.models.model_base import NonUnicodeString


class AcctivateProductVendor(db.Model):
    __tablename__ = 'acctivate_product_vendor'
    __bind_key__ = 'ordersDB'

    sku = Column(Unicode(128), nullable=False, primary_key=True)
    brand = Column(Unicode(64))
    cost = Column(Numeric(18,2))
    _product_name = Column(Unicode(128))
    vendor = Column(Unicode(64))
    upc = Column(String(32))
    list_price = Column(Numeric(18,2))
    normalized_sku = Column(String(159))



class AmazonData(db.Model):
    __tablename__ = 'amazon_data'
    __bind_key__ = 'ordersDB'

    sku = Column(Unicode(128))
    category = Column(Unicode)
    asin = Column(String(20))
    description = Column(Unicode)
    title = Column(Unicode)
    gender = Column(Unicode)
    brand = Column(Unicode(256))
    upc = Column(String(25))
    image_link = Column(Unicode)
    product_id = Column(Integer, primary_key=True)
    parent_sku = Column(Unicode(128))
    parent_asin = Column(String(20))
    status = Column(Unicode(20), nullable=False, server_default=FetchedValue())



class AmazonDataLog(db.Model):
    __tablename__ = 'amazon_data_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    column_name = Column(Unicode(128), nullable=False)
    old_value = Column(Unicode(128))
    new_value = Column(Unicode(128))
    user = Column(Unicode(128), nullable=False)
    timestamp = Column(DateTime, server_default=FetchedValue())



class BalancerAction(db.Model):
    __tablename__ = 'balancer_action'
    __bind_key__ = 'ordersDB'

    action_id = Column(Integer, primary_key=True)
    description = Column(Unicode(128), nullable=False)



class BalancerSubmissionResult(db.Model):
    __tablename__ = 'balancer_submission_result'
    __bind_key__ = 'ordersDB'

    result_id = Column(Integer, primary_key=True)
    description = Column(Unicode(128), nullable=False)



class Carrier(db.Model):
    __tablename__ = 'carrier'
    __bind_key__ = 'ordersDB'

    carrier = Column(Integer, primary_key=True)
    name = Column(Unicode(500), nullable=False)



class InventoryBalancerLog(db.Model):
    __tablename__ = 'inventory_balancer_log'
    __bind_key__ = 'ordersDB'

    log_id = Column(Integer, primary_key=True)
    guid_order_line = Column(ForeignKey('order_lines.guid_order_line'))
    sku = Column(String(159), nullable=False)
    total_submissions = Column(Integer, nullable=False)
    pending_submissions = Column(Integer, server_default=FetchedValue())
    locked_submissions = Column(Integer, server_default=FetchedValue())
    submission_ids = Column(NonUnicodeString, nullable=False)
    created = Column(DateTime, server_default=FetchedValue())
    from_warehouse = Column(BIT, nullable=False, server_default=FetchedValue())

    order_lines = relationship('OrderLines', primaryjoin='InventoryBalancerLog.guid_order_line == OrderLines.guid_order_line')



class InventoryBalancerSubmissionLog(db.Model):
    __tablename__ = 'inventory_balancer_submission_log'
    __bind_key__ = 'ordersDB'

    log_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, nullable=False)
    submission_qty = Column(Integer, nullable=False)
    submission_timestamp = Column(DateTime, nullable=False)
    submission_batch_id = Column(String(128))
    result_id = Column(ForeignKey('balancer_submission_result.result_id'), nullable=False)
    action_id = Column(Integer, nullable=False, server_default=FetchedValue())

    result = relationship('BalancerSubmissionResult', primaryjoin='InventoryBalancerSubmissionLog.result_id == BalancerSubmissionResult.result_id', backref='inventory_balancer_submission_logs')



class InventoryBalancerSubmissions(db.Model):
    __tablename__ = 'inventory_balancer_submissions'
    __bind_key__ = 'ordersDB'

    submission_id = Column(Integer, primary_key=True)
    sku = Column(Unicode(128), nullable=False)
    sales_channel = Column(ForeignKey('sales_channel.sales_channel'), nullable=False)
    submission_count = Column(Integer, server_default=FetchedValue())
    action_id = Column(ForeignKey('balancer_action.action_id'), server_default=FetchedValue())
    created = Column(DateTime, server_default=FetchedValue())

    action = relationship('BalancerAction', primaryjoin='InventoryBalancerSubmissions.action_id == BalancerAction.action_id', backref='inventory_balancer_submissionss')
    sales_channel1 = relationship('SalesChannel', primaryjoin='InventoryBalancerSubmissions.sales_channel == SalesChannel.sales_channel', backref='inventory_balancer_submissionss')



class InventoryLocationsAvaiable(db.Model):
    __tablename__ = 'inventory_locations_avaiable'
    __bind_key__ = 'inventoryDB'

    Row = Column(String(10), nullable=False, primary_key=True)
    Level = Column(String(10), nullable=False)
    Col = Column(String(10), nullable=False)
    Qty = Column(Integer, nullable=False)
    UPC = Column(String(25))
    lID = Column(Integer, nullable=False)
    rev = Column(String(50))
    imageURL = Column(Unicode(4000))
    shortUPC = Column(String(10))
    location = Column(String(30), nullable=False)
    QTY_Avail = Column(Integer)
    SKU = Column(Unicode(128))
    sku_seg = Column(Unicode(4000))



class InventoryLocationsSpecial(db.Model):
    __tablename__ = 'inventory_locations_special'
    __bind_key__ = 'inventoryDB'

    Row = Column(String(10), nullable=False, primary_key=True)
    Level = Column(String(10), nullable=False)
    Col = Column(String(10), nullable=False)
    Qty = Column(Integer, nullable=False)
    UPC = Column(String(25))
    lID = Column(Integer, nullable=False)
    rev = Column(String(50))
    imageURL = Column(Unicode(4000))
    shortUPC = Column(String(10))
    location = Column(String(30), nullable=False)
    QTY_Avail = Column(Integer)
    SKU = Column(Unicode(128))
    sku_seg = Column(Unicode(4000))



class LinkedOrderLines(db.Model):
    __tablename__ = 'linked_order_lines'
    __bind_key__ = 'ordersDB'

    linked_order_id = Column(Unicode(100), nullable=False)
    linked_order_line_id = Column(Unicode(120), primary_key=True)
    guid_order_line = Column(ForeignKey('order_lines.guid_order_line'), nullable=False)
    linked_sales_channel = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, server_default=FetchedValue())

    order_lines = relationship('OrderLines', primaryjoin='LinkedOrderLines.guid_order_line == OrderLines.guid_order_line')



class MerchantOrderId(db.Model):
    __tablename__ = 'merchant_order_id'
    __bind_key__ = 'ordersDB'

    order_id = Column(Unicode(100), primary_key=True, nullable=False)
    merchant_order_id = Column(Integer, primary_key=True, nullable=False)
    date_added = Column(DateTime)
    submitted_date = Column(DateTime)
    submitted = Column(BIT, server_default=FetchedValue())
    feed_submission_id = Column(Unicode(20))



class OrderFlags(db.Model):
    __tablename__ = 'order_flags'
    __bind_key__ = 'ordersDB'

    order_id = Column(ForeignKey('orders.order_id'), primary_key=True)
    order_status = Column(Integer)
    processing_status = Column(Integer, nullable=False, server_default=FetchedValue())
    referring_order = Column(Integer)
    is_prime = Column(BIT)
    is_premium = Column(BIT)
    shipping_priority = Column(Unicode(128))



class OrderLineFlagsLog(db.Model):
    __tablename__ = 'order_line_flags_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = Column(Integer, primary_key=True)
    guid_order_line = Column(Unicode(40), nullable=False)
    column_name = Column(Unicode(128), nullable=False)
    old_value = Column(Unicode(128))
    new_value = Column(Unicode(128))
    user = Column(Unicode(128), nullable=False)
    timestamp = Column(DateTime, server_default=FetchedValue())



class OrderLineHierarchy(db.Model):
    __tablename__ = 'order_line_hierarchy'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(40), nullable=False, primary_key=True)
    parent_guid_order_line = Column(Unicode(40))



class OrderLineStatus(db.Model):
    __tablename__ = 'order_line_status'
    __bind_key__ = 'ordersDB'

    status = Column(Integer, primary_key=True)
    description = Column(Unicode(500), nullable=False)



class OrderLineStatusExclusions(db.Model):
    __tablename__ = 'order_line_status_exclusions'
    __bind_key__ = 'ordersDB'

    order_line_status = Column(Integer, nullable=False, primary_key=True)
    exclusion_reason = Column(Unicode)



class OrderLineTypeAssignment(db.Model):
    __tablename__ = 'order_line_type_assignment'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(120), nullable=False)
    last_order_line_type = Column(Unicode(1))
    new_order_line_type = Column(Unicode(1))
    user_name = Column(Unicode(120))
    last_mod_time = Column(DateTime)
    current_mod_time = Column(DateTime)
    id = Column(Integer, primary_key=True)



class OrderLineTypeExclusions(db.Model):
    __tablename__ = 'order_line_type_exclusions'
    __bind_key__ = 'ordersDB'

    line_type = Column(Unicode(10), nullable=False, primary_key=True)
    exclusion_reason = Column(Unicode, nullable=False)



class OrderLines(db.Model):
    __tablename__ = 'order_lines'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(40), primary_key=True, server_default=FetchedValue())
    order_line_id = Column(Unicode(120), nullable=False)
    qty_ordered = Column(Integer, nullable=False)
    qty_shipped = Column(Integer)
    price = Column(Numeric(18, 2), nullable=False)
    tax = Column(Numeric(18, 2))
    shipping_price = Column(Numeric(18, 2))
    shipping_tax = Column(Numeric(18, 2))
    created = Column(DateTime)
    sku = Column(String(159))
    order_id = Column(ForeignKey('orders.order_id'), nullable=False)

    order = relationship('Orders', primaryjoin='OrderLines.order_id == Orders.order_id')
    order_line_flags = relationship('OrderLineFlags', primaryjoin='foreign(OrderLines.guid_order_line) == remote(OrderLineFlags.guid_order_line)',
                                       foreign_keys='OrderLineFlags.guid_order_line', post_update=True)
    product = relationship('TbProducts', primaryjoin='foreign(OrderLines.sku) == remote(TbProducts.normalized_sku)')
    shipments = relationship('ShipmentLines', uselist=True)

    @hybrid_property
    def tracking_number(self):
        return self.shipments[0].tracking_number if self.shipments else None

class OrderLineFlags(db.Model):
    __tablename__ = 'order_line_flags'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(ForeignKey('order_lines.guid_order_line'), primary_key=True)
    line_type = Column(Unicode(10))
    qty_shipped = Column(Integer)
    processed_date = Column(DateTime)
    purchase_order_number = Column(Unicode(128))
    order_line_status = Column(Unicode(10), server_default=FetchedValue())
    exported = Column(BIT)
    date_exported = Column(DateTime)
    username = Column(Unicode(256))
    notes = Column(Unicode)
    linked_order_id = Column(Unicode(128))
    promise_date = Column(DateTime)
    fulfillment_warehouse_id = Column(ForeignKey('warehouses.warehouse_id'), server_default=FetchedValue())
    is_premium = Column(BIT, nullable=False, server_default=FetchedValue())
    shipping_priority = Column(Unicode(128))

    fulfillment_warehouse = relationship('Warehouses', primaryjoin='foreign(OrderLineFlags.fulfillment_warehouse_id) == remote(Warehouses.warehouse_id)')
    OrderLineStatus = relationship('OrderLineStatus', primaryjoin='foreign(OrderLineFlags.order_line_status) == remote(OrderLineStatus.status)')

class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    __bind_key__ = 'ordersDB'

    status = Column(Integer, primary_key=True)
    description = Column(Unicode(500), nullable=False)



class OrderView(db.Model):
    __tablename__ = 'order_view'
    __bind_key__ = 'ordersDB'

    order_id = Column(Unicode(100), nullable=False, primary_key=True)
    purchase_date = Column(DateTime, nullable=False)
    ship_name = Column(Unicode(500), nullable=False)
    ship_phone = Column(Unicode(100))
    ship_address_1 = Column(Unicode(500), nullable=False)
    ship_address_2 = Column(Unicode(500))
    ship_address_3 = Column(Unicode(500))
    ship_city = Column(Unicode(500))
    ship_state = Column(Unicode(500))
    ship_postal_code = Column(Unicode(100))
    ship_country = Column(Unicode(500), nullable=False)
    buyer_name = Column(Unicode(500))
    buyer_phone = Column(Unicode(100))
    buyer_address_1 = Column(Unicode(500))
    buyer_address_2 = Column(Unicode(500))
    buyer_address_3 = Column(Unicode(500))
    buyer_city = Column(Unicode(500))
    buyer_state = Column(Unicode(500))
    buyer_postal_code = Column(Unicode(100))
    buyer_country = Column(Unicode(500))
    buyer_email = Column(Unicode(500))
    ship_email = Column(Unicode(500))
    sales_order_number = Column(Integer, nullable=False)
    sales_channel = Column(Integer)
    Created = Column(DateTime)
    order_status = Column(Integer)
    processing_status = Column(Integer, nullable=False)
    total_qty = Column(Integer)
    populated_qty = Column(Integer, nullable=False)
    order_total = Column(Numeric(18, 2))



class Orders(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = 'ordersDB'

    order_id = Column(Unicode(100), primary_key=True)
    purchase_date = Column(DateTime, nullable=False)
    ship_name = Column(Unicode(500), nullable=False)
    ship_phone = Column(Unicode(100))
    ship_address_1 = Column(Unicode(500), nullable=False)
    ship_address_2 = Column(Unicode(500))
    ship_address_3 = Column(Unicode(500))
    ship_city = Column(Unicode(500))
    ship_state = Column(Unicode(500))
    ship_postal_code = Column(Unicode(100))
    ship_country = Column(Unicode(500), nullable=False)
    buyer_name = Column(Unicode(500))
    buyer_phone = Column(Unicode(100))
    buyer_address_1 = Column(Unicode(500))
    buyer_address_2 = Column(Unicode(500))
    buyer_address_3 = Column(Unicode(500))
    buyer_city = Column(Unicode(500))
    buyer_state = Column(Unicode(500))
    buyer_postal_code = Column(Unicode(100))
    buyer_country = Column(Unicode(500))
    buyer_email = Column(Unicode(500))
    ship_email = Column(Unicode(500))
    sales_order_number = Column(Integer, nullable=False)
    sales_channel = Column(Integer)
    Created = Column(DateTime, server_default=FetchedValue())
    total_qty = Column(Integer)

    @hybrid_property
    def email(self):
        return self.ship_email or self.buyer_email

    order_flags = relationship('OrderFlags',
                                  primaryjoin='foreign(Orders.order_id) == remote(OrderFlags.order_id)')
    SalesChannel = relationship('SalesChannel',
                                  primaryjoin='foreign(Orders.sales_channel) == remote(SalesChannel.sales_channel)')

class PackageCondition(db.Model):
    __tablename__ = 'package_condition'
    __bind_key__ = 'ordersDB'

    condition = Column(Integer, nullable=False, primary_key=True)
    description = Column(Unicode(512), nullable=False)



class ProductAliasGroups(db.Model):
    __tablename__ = 'product_alias_groups'
    __bind_key__ = 'ordersDB'

    alias_id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)



class ProductCondition(db.Model):
    __tablename__ = 'product_condition'
    __bind_key__ = 'ordersDB'

    condition = Column(Integer, nullable=False, primary_key=True)
    description = Column(Unicode(512), nullable=False)



class ProductCost(db.Model):
    __tablename__ = 'product_cost'
    __bind_key__ = 'ordersDB'

    UPC = Column(String(32))
    _shortUPC = Column(String(10))
    ProductID = Column(Unicode(128), nullable=False, primary_key=True)
    _Cost = Column(Numeric(18, 2))
    ListPrice = Column(Numeric(18, 2))
    _Vendor = Column(Unicode(64))



class PullLocation(db.Model):
    __tablename__ = 'pull_location'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(40))
    location = Column(Unicode(50))
    qty = Column(Integer)
    lid = Column(Integer, primary_key=True)



class ReturnAction(db.Model):
    __tablename__ = 'return_action'
    __bind_key__ = 'ordersDB'

    action = Column(Integer, primary_key=True)
    description = Column(Unicode(512))



class ReturnActions(db.Model):
    __tablename__ = 'return_actions'
    __bind_key__ = 'ordersDB'

    action_id = Column(Integer, primary_key=True)
    name = Column(Unicode(127))



class ReturnConditions(db.Model):
    __tablename__ = 'return_conditions'
    __bind_key__ = 'ordersDB'

    condition_id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))



class ReturnDetails(db.Model):
    __tablename__ = 'return_details'
    __bind_key__ = 'ordersDB'

    return_line_id = Column(Integer, primary_key=True)
    guid_order_line = Column(Unicode(40), nullable=False)
    replacement_so_number = Column(Unicode(128))
    replacement_po_number = Column(Unicode(128))
    return_status = Column(Integer, nullable=False)
    return_action = Column(Integer, nullable=False)
    package_condition = Column(Integer)
    product_condition = Column(Integer)
    replacement_sku = Column(Unicode(128))
    created = Column(DateTime, server_default=FetchedValue())
    replacement_order_id = Column(Unicode(128))
    notes = Column(Unicode)



class ReturnLineFlags(db.Model):
    __tablename__ = 'return_line_flags'
    __bind_key__ = 'ordersDB'

    return_id = Column(Integer, primary_key=True)
    guid_order_line = Column(ForeignKey('order_lines.guid_order_line'), nullable=False)
    process_id = Column(ForeignKey('return_process_level.process_id'), nullable=False)
    created_date = Column(DateTime, nullable=False)
    closed_date = Column(DateTime)
    return_tracking_number = Column(Unicode)
    condition = Column(Integer, nullable=False)
    return_action = Column(ForeignKey('return_actions.action_id'), nullable=False)
    notes = Column(Unicode)
    ra_number = Column(Unicode)
    return_qty = Column(Integer, nullable=False)

    order_lines = relationship('OrderLines', primaryjoin='ReturnLineFlags.guid_order_line == OrderLines.guid_order_line')
    process = relationship('ReturnProcessLevel', primaryjoin='ReturnLineFlags.process_id == ReturnProcessLevel.process_id', backref='return_line_flagss')
    return_actions = relationship('ReturnActions', primaryjoin='ReturnLineFlags.return_action == ReturnActions.action_id', backref='return_line_flagss')



class ReturnLineFlagsLog(db.Model):
    __tablename__ = 'return_line_flags_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = Column(Integer, primary_key=True)
    return_id = Column(Integer, nullable=False)
    column_name = Column(Unicode(128), nullable=False)
    old_value = Column(Unicode)
    new_value = Column(Unicode)
    user = Column(Unicode(128), nullable=False)
    timestamp = Column(DateTime, server_default=FetchedValue())



class ReturnProcessLevel(db.Model):
    __tablename__ = 'return_process_level'
    __bind_key__ = 'ordersDB'

    process_id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))



class ReturnStatus(db.Model):
    __tablename__ = 'return_status'
    __bind_key__ = 'ordersDB'

    status = Column(Integer, primary_key=True)
    description = Column(Unicode(512))



class ReturnsToReplacements(db.Model):
    __tablename__ = 'returns_to_replacements'
    __bind_key__ = 'ordersDB'

    replacement_id = Column(Integer, primary_key=True)
    return_id = Column(Integer, nullable=False)
    replacement_sku = Column(String(159), nullable=False)
    replacement_qty = Column(Integer, nullable=False)
    replacement_guid_line = Column(Unicode(40))



class ReturnsToReplacementsLog(db.Model):
    __tablename__ = 'returns_to_replacements_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = Column(Integer, primary_key=True)
    replacement_id = Column(Integer, nullable=False)
    return_id = Column(Integer, nullable=False)
    column_name = Column(Unicode(128), nullable=False)
    old_value = Column(Unicode(128))
    new_value = Column(Unicode(128))
    user = Column(Unicode(128), nullable=False)
    timestamp = Column(DateTime, server_default=FetchedValue())



class SalesChannel(db.Model):
    __tablename__ = 'sales_channel'
    __bind_key__ = 'ordersDB'

    sales_channel = Column(Integer, primary_key=True)
    description = Column(Unicode(100), nullable=False, unique=True)
    abbr = Column(Unicode(10), unique=True)
    service_id = Column(Unicode(50), unique=True)
    balanceable = Column(BIT, nullable=False, server_default=FetchedValue())
    enabled = Column(BIT, nullable=False, server_default=FetchedValue())
    product_alias_group = Column(Integer, nullable=False, server_default=FetchedValue())
    is_cross_insert = Column(BIT, nullable=False, server_default=FetchedValue())



class SalesOrderSubmissions(db.Model):
    __tablename__ = 'sales_order_submissions'
    __bind_key__ = 'ordersDB'

    so_submission_id = Column(Integer, primary_key=True)
    order_id = Column(Unicode(100), nullable=False)
    submission_count = Column(Integer, server_default=FetchedValue())
    failed_submission_count = Column(Integer, server_default=FetchedValue())
    last_submission_date = Column(DateTime)
    last_submission_id = Column(Unicode(100))
    sales_channel = Column(Integer, nullable=False)



class ScanLogWorkingLocations(db.Model):
    __tablename__ = 'scan_log_working_locations'
    __bind_key__ = 'ordersDB'

    UPC = Column(String(25), nullable=False, primary_key=True)
    Qty = Column(Integer, nullable=False)
    Old_Qty = Column(Integer)
    location = Column(String(30))
    date_scanned = Column(DateTime, nullable=False)
    old_location = Column(String(30))
    new_lID = Column(Integer)
    old_lID = Column(Integer)



class ShipFlags(db.Model):
    __tablename__ = 'ship_flags'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(40))
    promise_date = Column(DateTime)
    id = Column(Integer, primary_key=True)



class ShipmentLineSubmissions(db.Model):
    __tablename__ = 'shipment_line_submissions'
    __bind_key__ = 'ordersDB'

    shipment_line_id = Column(Integer, nullable=False)
    shipment_submission_id = Column(Integer, primary_key=True)
    sales_channel = Column(Integer, nullable=False)
    submission_count = Column(Integer, server_default=FetchedValue())
    failed_submission_count = Column(Integer, server_default=FetchedValue())
    order_id = Column(Unicode(100))
    order_line_id = Column(Unicode(120))
    last_submission_date = Column(DateTime)



class ShipmentLines(db.Model):
    __tablename__ = 'shipment_lines'
    __bind_key__ = 'ordersDB'

    shipment_line_id = Column(Integer, primary_key=True)
    shipment_line_status = Column(Integer, nullable=False)
    shipment_line_type = Column(Integer, nullable=False)
    tracking_number = Column(Unicode(128))
    service_level = Column(Unicode(128))
    weight = Column(Numeric(12,5))
    package_count = Column(Integer, server_default=FetchedValue())
    ship_timestamp = Column(DateTime, nullable=False)
    promise_date = Column(DateTime)
    created = Column(DateTime, nullable=False, server_default=FetchedValue())
    guid_order_line = Column(ForeignKey('order_lines.guid_order_line'), nullable=False)
    carrier = Column(Integer)

    order_lines = relationship('OrderLines', primaryjoin='ShipmentLines.guid_order_line == OrderLines.guid_order_line')



class ShipmentLinesLog(db.Model):
    __tablename__ = 'shipment_lines_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = Column(Integer, primary_key=True)
    guid_order_line = Column(Unicode(40), nullable=False)
    old_shipment = Column(NonUnicodeString)
    new_shipment = Column(NonUnicodeString, nullable=False)
    timestamp = Column(DateTime)
    username = Column(Unicode(128))



class Shipments(db.Model):
    __tablename__ = 'shipments'
    __bind_key__ = 'ordersDB'

    guid_order_line = Column(Unicode(40), nullable=False)
    carrier = Column(Integer)
    tracking_number = Column(Unicode(128))
    service_level = Column(Unicode(128))
    weight = Column(Numeric(12,6))
    package_count = Column(Integer)
    ship_timestamp = Column(DateTime)
    id = Column(Integer, primary_key=True)
    Created = Column(DateTime, server_default=FetchedValue())
    submission_count = Column(Integer, server_default=FetchedValue())
    failed = Column(BIT, server_default=FetchedValue())
    promise_date = Column(DateTime)



class ShippingRules(db.Model):
    __tablename__ = 'shipping_rules'
    __bind_key__ = 'ordersDB'

    supplier = Column(Unicode(100))
    edi = Column(BIT)
    apo = Column(BIT)
    non_48 = Column(BIT)
    warehouse_shipment = Column(BIT)
    tranship_brand = Column(BIT)
    email_brand = Column(BIT)
    dropship_fee = Column(Unicode(10))
    restocking_fee = Column(Unicode(10))
    leadtime = Column(Unicode(8))
    brand = Column(String(41))
    id = Column(Integer, primary_key=True)
    po_override = Column(Unicode(10))
    valid_sales_channels = Column(NonUnicodeString)
    normalized_brand = Column(String(8000), server_default=FetchedValue())
    normalized_supplier = Column(Unicode(4000), server_default=FetchedValue())
    fulfillment_warehouses = Column(NonUnicodeString)



class SpecialOrderPo(db.Model):
    __tablename__ = 'special_order_po'
    __bind_key__ = 'ordersDB'

    id = Column(Integer, primary_key=True)
    brand = Column(String(199))
    date_processed = Column(DateTime)
    order_session = Column(String(199))
    sPO = Column(String(207))
    bekir_sPO = Column(String(209))
    short_sPO = Column(String(209))
    numericPO = Column(Integer)
    scanned_in = Column(String(199))
    sku = Column(String(128))
    Merchant_Order_Id = Column(Integer)
    scanned_in_date = Column(DateTime)
    numeric_po = Column(Integer)
    scan_out_by = Column(String(199))
    quantity_purchased = Column(Integer)
    purchase_date = Column(DATETIMEOFFSET)
    EDI = Column(String(50))
    order_id = Column(Unicode(128))
    order_item_id = Column(Unicode(128))
    guid_order_line = Column(Unicode(40), server_default=FetchedValue())



class TbProduct(db.Model):
    __tablename__ = 'tbProduct'
    __bind_key__ = 'productsDB'

    ProductID = Column(Unicode(128), nullable=False, primary_key=True)
    upc = Column(String(32))
    _Vendor = Column(Unicode(64))
    _supplier = Column(Unicode(64))
    _product_name = Column(Unicode(128))
    _shortUPC = Column(String(10))
    description = Column(Unicode)
    _cost = Column(Numeric(18, 2))
    GUIDProduct = Column(String(40))
    color = Column(Unicode(100))
    size = Column(String(64))
    ProductType = Column(String(16))
    gender = Column(String(64))
    _altSKU = Column(Unicode(128))
    normalized_brand = Column(Unicode(64))
    normalized_supplier = Column(Unicode(64))
    normalized_sku = Column(String(159))



class TbProductPricing(db.Model):
    __tablename__ = 'tbProductPricing'
    __bind_key__ = 'productsDB'

    upc = Column(String(32), primary_key=True)
    price = Column(Numeric(18,2))
    cost = Column(Numeric(18,2), nullable=False)



class TbProducts(db.Model):
    __tablename__ = 'tbProducts'
    __bind_key__ = 'productsDB'

    sku = Column(Unicode(128), primary_key=True)
    upc = Column(String(32))
    brand = Column(Unicode(64))
    supplier = Column(Unicode(64))
    gender = Column(String(64))
    product_name = Column(Unicode(128))
    product_type = Column(String(16))
    checksum = Column(Integer)
    google_category = Column(Unicode(256))
    _shortUPC = Column(String(10), server_default=FetchedValue())
    description = Column(Unicode)
    size = Column(String(64))
    GUIDProduct = Column(String(40))
    GUIDVendor = Column(String(40))
    alt_sku = Column(Unicode(128))
    normalized_brand = Column(Unicode(64), server_default=FetchedValue())
    normalized_supplier = Column(Unicode(64), server_default=FetchedValue())
    color = Column(Unicode(100))
    normalized_sku = Column(String(159), server_default=FetchedValue())
    last_updated = Column(DateTime, nullable=False, server_default=FetchedValue())

    product_pricing = relationship('TbProductPricing', primaryjoin='foreign(TbProducts.upc) == remote(TbProductPricing.upc)')
    shipping_rules = relationship('ShippingRules',
            primaryjoin='(foreign(TbProducts.brand) == remote(ShippingRules.brand)) and (foreign(TbProducts.supplier) == remote(ShippingRules.supplier))')

class TbVendor(db.Model):
    __tablename__ = 'tbVendor'
    __bind_key__ = 'productsDB'

    vendor = Column(Unicode(64), primary_key=True)
    GUIDVendor = Column(String(40))



class TblInvLocations(db.Model):
    __tablename__ = 'tblInvLocations'
    __bind_key__ = 'inventoryDB'

    lID = Column(Integer, primary_key=True)
    Row = Column(String(10), nullable=False)
    Level = Column(String(10), nullable=False)
    Col = Column(String(10), nullable=False)
    Qty = Column(Integer, nullable=False)
    rev = Column(String(50))
    UPC = Column(String(25))
    guidItemLoc = Column(Integer, server_default=FetchedValue())
    shortUPC = Column(String(10), server_default=FetchedValue())
    lastModTime = Column(DateTime, server_default=FetchedValue())
    QTY_Avail = Column(Integer)



class VInvLocationsDev(db.Model):
    __tablename__ = 'vInvLocationsDev'
    __bind_key__ = 'inventoryDB'

    Row = Column(String(10), nullable=False, primary_key=True)
    Level = Column(String(10), nullable=False)
    Col = Column(String(10), nullable=False)
    Qty = Column(Integer, nullable=False)
    UPC = Column(String(25))
    lID = Column(Integer, nullable=False)
    rev = Column(String(50))
    SKU = Column(Unicode(4000))
    imageURL = Column(Unicode(4000))
    shortUPC = Column(String(10))
    location = Column(String(30), nullable=False)
    QTY_Avail = Column(Integer)
    sku_seg = Column(Unicode(4000))



class VProductUrls(db.Model):
    __tablename__ = 'vProductUrls'
    __bind_key__ = 'inventoryDB'

    UPC = Column(String(32), primary_key=True)
    _shortUPC = Column(String(10))
    imageURL = Column(Unicode(4000))



class VReturnsDetails(db.Model):
    __tablename__ = 'vReturns_Details'
    __bind_key__ = 'ordersDB'

    return_line_id = Column(Integer, nullable=False)
    replacement_so_number = Column(Unicode(128))
    replacement_po_number = Column(Unicode(128))
    returns_status = Column(Unicode(512))
    order_id = Column(Unicode(100))
    order_line_id = Column(Unicode(120))
    package_condition = Column(Unicode(512))
    product_condition = Column(Unicode(512))
    returns_action = Column(Unicode(512))
    notes = Column(Unicode)
    replacement_sku = Column(Unicode(128))
    created = Column(DateTime)
    guid_order_line = Column(Unicode(40), nullable=False, primary_key=True)
    sku = Column(String(159))
    qty_ordered = Column(Integer)
    purchase_date = Column(DateTime)
    sales_channel = Column(Integer)
    sales_order_number = Column(Integer)
    ship_name = Column(Unicode(500))
    ship_phone = Column(Unicode(100))
    ship_address_1 = Column(Unicode(500))
    ship_address_2 = Column(Unicode(500))
    ship_address_3 = Column(Unicode(500))
    ship_city = Column(Unicode(500))
    ship_state = Column(Unicode(500))
    ship_postal_code = Column(Unicode(100))
    ship_country = Column(Unicode(500))
    replacement_order_id = Column(Unicode(128))
    replacement_GUID_order_line = Column(Unicode(40))
    tracking_number = Column(Unicode(128))
    ship_timestamp = Column(DateTime)



class Warehouses(db.Model):
    __tablename__ = 'warehouses'
    __bind_key__ = 'ordersDB'

    warehouse_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    abbr = Column(String(10), nullable=False)
    enabled = Column(BIT, nullable=False, server_default=FetchedValue())



class ZipCities(db.Model):
    __tablename__ = 'zip_cities'
    __bind_key__ = 'ordersDB'

    zip_code = Column(String(25), primary_key=True)
    zip_cities = Column(Unicode, nullable=False)



class ZipCodes(db.Model):
    __tablename__ = 'zip_codes'
    __bind_key__ = 'ordersDB'

    zip_code = Column(String(25), nullable=False)
    state = Column(String(5), nullable=False)
    id = Column(Integer, primary_key=True)
