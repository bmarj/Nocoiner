# coding: utf-8
from api.models.model_base import db, BIT, DECIMAL, NUMERIC, DATETIMEOFFSET, MetaData
from sqlalchemy.ext.hybrid import hybrid_property

class AcctivateProductVendor(db.Model):
    __tablename__ = 'acctivate_product_vendor'
    __bind_key__ = 'ordersDB'

    sku = db.Column(db.Unicode(128), nullable=False, primary_key=True)
    brand = db.Column(db.Unicode(64))
    cost = db.Column(db.Numeric(18,2))
    _product_name = db.Column(db.Unicode(128))
    vendor = db.Column(db.Unicode(64))
    upc = db.Column(db.String(32))
    list_price = db.Column(db.Numeric(18,2))
    normalized_sku = db.Column(db.String(159))



class AmazonData(db.Model):
    __tablename__ = 'amazon_data'
    __bind_key__ = 'ordersDB'

    sku = db.Column(db.Unicode(128))
    category = db.Column(db.Unicode)
    asin = db.Column(db.String(20))
    description = db.Column(db.Unicode)
    title = db.Column(db.Unicode)
    gender = db.Column(db.Unicode)
    brand = db.Column(db.Unicode(256))
    upc = db.Column(db.String(25))
    image_link = db.Column(db.Unicode)
    product_id = db.Column(db.BigInteger, primary_key=True)
    parent_sku = db.Column(db.Unicode(128))
    parent_asin = db.Column(db.String(20))
    status = db.Column(db.Unicode(20), nullable=False, server_default=db.FetchedValue())



class AmazonDataLog(db.Model):
    __tablename__ = 'amazon_data_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, nullable=False)
    column_name = db.Column(db.Unicode(128), nullable=False)
    old_value = db.Column(db.Unicode(128))
    new_value = db.Column(db.Unicode(128))
    user = db.Column(db.Unicode(128), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.FetchedValue())



class BalancerAction(db.Model):
    __tablename__ = 'balancer_action'
    __bind_key__ = 'ordersDB'

    action_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(128), nullable=False)



class BalancerSubmissionResult(db.Model):
    __tablename__ = 'balancer_submission_result'
    __bind_key__ = 'ordersDB'

    result_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(128), nullable=False)



class Carrier(db.Model):
    __tablename__ = 'carrier'
    __bind_key__ = 'ordersDB'

    carrier = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(500), nullable=False)



class InventoryBalancerLog(db.Model):
    __tablename__ = 'inventory_balancer_log'
    __bind_key__ = 'ordersDB'

    log_id = db.Column(db.Integer, primary_key=True)
    guid_order_line = db.Column(db.ForeignKey('order_lines.guid_order_line'))
    sku = db.Column(db.String(159), nullable=False)
    total_submissions = db.Column(db.Integer, nullable=False)
    pending_submissions = db.Column(db.Integer, server_default=db.FetchedValue())
    locked_submissions = db.Column(db.Integer, server_default=db.FetchedValue())
    submission_ids = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, server_default=db.FetchedValue())
    from_warehouse = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())

    order_lines = db.relationship('OrderLines', primaryjoin='InventoryBalancerLog.guid_order_line == OrderLines.guid_order_line')



class InventoryBalancerSubmissionLog(db.Model):
    __tablename__ = 'inventory_balancer_submission_log'
    __bind_key__ = 'ordersDB'

    log_id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, nullable=False)
    submission_qty = db.Column(db.Integer, nullable=False)
    submission_timestamp = db.Column(db.DateTime, nullable=False)
    submission_batch_id = db.Column(db.String(128))
    result_id = db.Column(db.ForeignKey('balancer_submission_result.result_id'), nullable=False)
    action_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    result = db.relationship('BalancerSubmissionResult', primaryjoin='InventoryBalancerSubmissionLog.result_id == BalancerSubmissionResult.result_id', backref='inventory_balancer_submission_logs')



class InventoryBalancerSubmissions(db.Model):
    __tablename__ = 'inventory_balancer_submissions'
    __bind_key__ = 'ordersDB'

    submission_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Unicode(128), nullable=False)
    sales_channel = db.Column(db.ForeignKey('sales_channel.sales_channel'), nullable=False)
    submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    action_id = db.Column(db.ForeignKey('balancer_action.action_id'), server_default=db.FetchedValue())
    created = db.Column(db.DateTime, server_default=db.FetchedValue())

    action = db.relationship('BalancerAction', primaryjoin='InventoryBalancerSubmissions.action_id == BalancerAction.action_id', backref='inventory_balancer_submissionss')
    sales_channel1 = db.relationship('SalesChannel', primaryjoin='InventoryBalancerSubmissions.sales_channel == SalesChannel.sales_channel', backref='inventory_balancer_submissionss')



class InventoryLocationsAvaiable(db.Model):
    __tablename__ = 'inventory_locations_avaiable'
    __bind_key__ = 'inventoryDB'

    Row = db.Column(db.String(10), nullable=False, primary_key=True)
    Level = db.Column(db.String(10), nullable=False)
    Col = db.Column(db.String(10), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    UPC = db.Column(db.String(25))
    lID = db.Column(db.BigInteger, nullable=False)
    rev = db.Column(db.String(50))
    imageURL = db.Column(db.Unicode(4000))
    shortUPC = db.Column(db.String(10))
    location = db.Column(db.String(30), nullable=False)
    QTY_Avail = db.Column(db.Integer)
    SKU = db.Column(db.Unicode(128))
    sku_seg = db.Column(db.Unicode(4000))



class InventoryLocationsSpecial(db.Model):
    __tablename__ = 'inventory_locations_special'
    __bind_key__ = 'inventoryDB'

    Row = db.Column(db.String(10), nullable=False, primary_key=True)
    Level = db.Column(db.String(10), nullable=False)
    Col = db.Column(db.String(10), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    UPC = db.Column(db.String(25))
    lID = db.Column(db.BigInteger, nullable=False)
    rev = db.Column(db.String(50))
    imageURL = db.Column(db.Unicode(4000))
    shortUPC = db.Column(db.String(10))
    location = db.Column(db.String(30), nullable=False)
    QTY_Avail = db.Column(db.Integer)
    SKU = db.Column(db.Unicode(128))
    sku_seg = db.Column(db.Unicode(4000))



class LinkedOrderLines(db.Model):
    __tablename__ = 'linked_order_lines'
    __bind_key__ = 'ordersDB'

    linked_order_id = db.Column(db.Unicode(100), nullable=False)
    linked_order_line_id = db.Column(db.Unicode(120), primary_key=True)
    guid_order_line = db.Column(db.ForeignKey('order_lines.guid_order_line'), nullable=False)
    linked_sales_channel = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    order_lines = db.relationship('OrderLines', primaryjoin='LinkedOrderLines.guid_order_line == OrderLines.guid_order_line')



class MerchantOrderId(db.Model):
    __tablename__ = 'merchant_order_id'
    __bind_key__ = 'ordersDB'

    order_id = db.Column(db.Unicode(100), primary_key=True, nullable=False)
    merchant_order_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    date_added = db.Column(db.DateTime)
    submitted_date = db.Column(db.DateTime)
    submitted = db.Column(db.BIT, server_default=db.FetchedValue())
    feed_submission_id = db.Column(db.Unicode(20))



class OrderFlags(db.Model):
    __tablename__ = 'order_flags'
    __bind_key__ = 'ordersDB'

    order_id = db.Column(db.ForeignKey('orders.order_id'), primary_key=True)
    order_status = db.Column(db.Integer)
    processing_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    referring_order = db.Column(db.BigInteger)
    is_prime = db.Column(db.BIT)
    is_premium = db.Column(db.BIT)
    shipping_priority = db.Column(db.Unicode(128))



class OrderLineFlagsLog(db.Model):
    __tablename__ = 'order_line_flags_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = db.Column(db.BigInteger, primary_key=True)
    guid_order_line = db.Column(db.Unicode(40), nullable=False)
    column_name = db.Column(db.Unicode(128), nullable=False)
    old_value = db.Column(db.Unicode(128))
    new_value = db.Column(db.Unicode(128))
    user = db.Column(db.Unicode(128), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.FetchedValue())



class OrderLineHierarchy(db.Model):
    __tablename__ = 'order_line_hierarchy'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(40), nullable=False, primary_key=True)
    parent_guid_order_line = db.Column(db.Unicode(40))



class OrderLineStatus(db.Model):
    __tablename__ = 'order_line_status'
    __bind_key__ = 'ordersDB'

    status = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(500), nullable=False)



class OrderLineStatusExclusions(db.Model):
    __tablename__ = 'order_line_status_exclusions'
    __bind_key__ = 'ordersDB'

    order_line_status = db.Column(db.Integer, nullable=False, primary_key=True)
    exclusion_reason = db.Column(db.Unicode)



class OrderLineTypeAssignment(db.Model):
    __tablename__ = 'order_line_type_assignment'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(120), nullable=False)
    last_order_line_type = db.Column(db.Unicode(1))
    new_order_line_type = db.Column(db.Unicode(1))
    user_name = db.Column(db.Unicode(120))
    last_mod_time = db.Column(db.DateTime)
    current_mod_time = db.Column(db.DateTime)
    id = db.Column(db.BigInteger, primary_key=True)



class OrderLineTypeExclusions(db.Model):
    __tablename__ = 'order_line_type_exclusions'
    __bind_key__ = 'ordersDB'

    line_type = db.Column(db.Unicode(10), nullable=False, primary_key=True)
    exclusion_reason = db.Column(db.Unicode, nullable=False)



class OrderLines(db.Model):
    __tablename__ = 'order_lines'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(40), primary_key=True, server_default=db.FetchedValue())
    order_line_id = db.Column(db.Unicode(120), nullable=False)
    qty_ordered = db.Column(db.Integer, nullable=False)
    qty_shipped = db.Column(db.Integer)
    price = db.Column(db.Numeric(18, 2), nullable=False)
    tax = db.Column(db.Numeric(18, 2))
    shipping_price = db.Column(db.Numeric(18, 2))
    shipping_tax = db.Column(db.Numeric(18, 2))
    created = db.Column(db.DateTime)
    sku = db.Column(db.String(159))
    order_id = db.Column(db.ForeignKey('orders.order_id'), nullable=False)

    order = db.relationship('Orders', primaryjoin='OrderLines.order_id == Orders.order_id')
    order_line_flags = db.relationship('OrderLineFlags', primaryjoin='foreign(OrderLines.guid_order_line) == remote(OrderLineFlags.guid_order_line)',
                                       foreign_keys='OrderLineFlags.guid_order_line', post_update=True)
    product = db.relationship('TbProducts', primaryjoin='foreign(OrderLines.sku) == remote(TbProducts.normalized_sku)')
    shipments = db.relationship('ShipmentLines', uselist=True)

    @hybrid_property
    def tracking_number(self):
        return self.shipments[0].tracking_number if self.shipments else None

class OrderLineFlags(db.Model):
    __tablename__ = 'order_line_flags'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.ForeignKey('order_lines.guid_order_line'), primary_key=True)
    line_type = db.Column(db.Unicode(10))
    qty_shipped = db.Column(db.Integer)
    processed_date = db.Column(db.DateTime)
    purchase_order_number = db.Column(db.Unicode(128))
    order_line_status = db.Column(db.Unicode(10), server_default=db.FetchedValue())
    exported = db.Column(db.BIT)
    date_exported = db.Column(db.DateTime)
    username = db.Column(db.Unicode(256))
    notes = db.Column(db.Unicode)
    linked_order_id = db.Column(db.Unicode(128))
    promise_date = db.Column(db.DateTime)
    fulfillment_warehouse_id = db.Column(db.ForeignKey('warehouses.warehouse_id'), server_default=db.FetchedValue())
    is_premium = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    shipping_priority = db.Column(db.Unicode(128))

    fulfillment_warehouse = db.relationship('Warehouses', primaryjoin='foreign(OrderLineFlags.fulfillment_warehouse_id) == remote(Warehouses.warehouse_id)')
    OrderLineStatus = db.relationship('OrderLineStatus', primaryjoin='foreign(OrderLineFlags.order_line_status) == remote(OrderLineStatus.status)')

class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    __bind_key__ = 'ordersDB'

    status = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(500), nullable=False)



class OrderView(db.Model):
    __tablename__ = 'order_view'
    __bind_key__ = 'ordersDB'

    order_id = db.Column(db.Unicode(100), nullable=False, primary_key=True)
    purchase_date = db.Column(db.DateTime, nullable=False)
    ship_name = db.Column(db.Unicode(500), nullable=False)
    ship_phone = db.Column(db.Unicode(100))
    ship_address_1 = db.Column(db.Unicode(500), nullable=False)
    ship_address_2 = db.Column(db.Unicode(500))
    ship_address_3 = db.Column(db.Unicode(500))
    ship_city = db.Column(db.Unicode(500))
    ship_state = db.Column(db.Unicode(500))
    ship_postal_code = db.Column(db.Unicode(100))
    ship_country = db.Column(db.Unicode(500), nullable=False)
    buyer_name = db.Column(db.Unicode(500))
    buyer_phone = db.Column(db.Unicode(100))
    buyer_address_1 = db.Column(db.Unicode(500))
    buyer_address_2 = db.Column(db.Unicode(500))
    buyer_address_3 = db.Column(db.Unicode(500))
    buyer_city = db.Column(db.Unicode(500))
    buyer_state = db.Column(db.Unicode(500))
    buyer_postal_code = db.Column(db.Unicode(100))
    buyer_country = db.Column(db.Unicode(500))
    buyer_email = db.Column(db.Unicode(500))
    ship_email = db.Column(db.Unicode(500))
    sales_order_number = db.Column(db.Integer, nullable=False)
    sales_channel = db.Column(db.Integer)
    Created = db.Column(db.DateTime)
    order_status = db.Column(db.Integer)
    processing_status = db.Column(db.Integer, nullable=False)
    total_qty = db.Column(db.Integer)
    populated_qty = db.Column(db.Integer, nullable=False)
    order_total = db.Column(db.Numeric(18, 2))



class Orders(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = 'ordersDB'

    order_id = db.Column(db.Unicode(100), primary_key=True)
    purchase_date = db.Column(db.DateTime, nullable=False)
    ship_name = db.Column(db.Unicode(500), nullable=False)
    ship_phone = db.Column(db.Unicode(100))
    ship_address_1 = db.Column(db.Unicode(500), nullable=False)
    ship_address_2 = db.Column(db.Unicode(500))
    ship_address_3 = db.Column(db.Unicode(500))
    ship_city = db.Column(db.Unicode(500))
    ship_state = db.Column(db.Unicode(500))
    ship_postal_code = db.Column(db.Unicode(100))
    ship_country = db.Column(db.Unicode(500), nullable=False)
    buyer_name = db.Column(db.Unicode(500))
    buyer_phone = db.Column(db.Unicode(100))
    buyer_address_1 = db.Column(db.Unicode(500))
    buyer_address_2 = db.Column(db.Unicode(500))
    buyer_address_3 = db.Column(db.Unicode(500))
    buyer_city = db.Column(db.Unicode(500))
    buyer_state = db.Column(db.Unicode(500))
    buyer_postal_code = db.Column(db.Unicode(100))
    buyer_country = db.Column(db.Unicode(500))
    buyer_email = db.Column(db.Unicode(500))
    ship_email = db.Column(db.Unicode(500))
    sales_order_number = db.Column(db.Integer, nullable=False)
    sales_channel = db.Column(db.Integer)
    Created = db.Column(db.DateTime, server_default=db.FetchedValue())
    total_qty = db.Column(db.Integer)

    @hybrid_property
    def email(self):
        return self.ship_email or self.buyer_email

    order_flags = db.relationship('OrderFlags',
                                  primaryjoin='foreign(Orders.order_id) == remote(OrderFlags.order_id)')
    SalesChannel = db.relationship('SalesChannel',
                                  primaryjoin='foreign(Orders.sales_channel) == remote(SalesChannel.sales_channel)')

class PackageCondition(db.Model):
    __tablename__ = 'package_condition'
    __bind_key__ = 'ordersDB'

    condition = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.Unicode(512), nullable=False)



class ProductAliasGroups(db.Model):
    __tablename__ = 'product_alias_groups'
    __bind_key__ = 'ordersDB'

    alias_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)



class ProductCondition(db.Model):
    __tablename__ = 'product_condition'
    __bind_key__ = 'ordersDB'

    condition = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.Unicode(512), nullable=False)



class ProductCost(db.Model):
    __tablename__ = 'product_cost'
    __bind_key__ = 'ordersDB'

    UPC = db.Column(db.String(32))
    _shortUPC = db.Column(db.String(10))
    ProductID = db.Column(db.Unicode(128), nullable=False, primary_key=True)
    _Cost = db.Column(db.Numeric(18, 2))
    ListPrice = db.Column(db.Numeric(18, 2))
    _Vendor = db.Column(db.Unicode(64))



class PullLocation(db.Model):
    __tablename__ = 'pull_location'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(40))
    location = db.Column(db.Unicode(50))
    qty = db.Column(db.Integer)
    lid = db.Column(db.Integer, primary_key=True)



class ReturnAction(db.Model):
    __tablename__ = 'return_action'
    __bind_key__ = 'ordersDB'

    action = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(512))



class ReturnActions(db.Model):
    __tablename__ = 'return_actions'
    __bind_key__ = 'ordersDB'

    action_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(127))



class ReturnConditions(db.Model):
    __tablename__ = 'return_conditions'
    __bind_key__ = 'ordersDB'

    condition_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))



class ReturnDetails(db.Model):
    __tablename__ = 'return_details'
    __bind_key__ = 'ordersDB'

    return_line_id = db.Column(db.BigInteger, primary_key=True)
    guid_order_line = db.Column(db.Unicode(40), nullable=False)
    replacement_so_number = db.Column(db.Unicode(128))
    replacement_po_number = db.Column(db.Unicode(128))
    return_status = db.Column(db.Integer, nullable=False)
    return_action = db.Column(db.Integer, nullable=False)
    package_condition = db.Column(db.Integer)
    product_condition = db.Column(db.Integer)
    replacement_sku = db.Column(db.Unicode(128))
    created = db.Column(db.DateTime, server_default=db.FetchedValue())
    replacement_order_id = db.Column(db.Unicode(128))
    notes = db.Column(db.Unicode)



class ReturnLineFlags(db.Model):
    __tablename__ = 'return_line_flags'
    __bind_key__ = 'ordersDB'

    return_id = db.Column(db.Integer, primary_key=True)
    guid_order_line = db.Column(db.ForeignKey('order_lines.guid_order_line'), nullable=False)
    process_id = db.Column(db.ForeignKey('return_process_level.process_id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    closed_date = db.Column(db.DateTime)
    return_tracking_number = db.Column(db.Unicode)
    condition = db.Column(db.Integer, nullable=False)
    return_action = db.Column(db.ForeignKey('return_actions.action_id'), nullable=False)
    notes = db.Column(db.Unicode)
    ra_number = db.Column(db.Unicode)
    return_qty = db.Column(db.Integer, nullable=False)

    order_lines = db.relationship('OrderLines', primaryjoin='ReturnLineFlags.guid_order_line == OrderLines.guid_order_line')
    process = db.relationship('ReturnProcessLevel', primaryjoin='ReturnLineFlags.process_id == ReturnProcessLevel.process_id', backref='return_line_flagss')
    return_actions = db.relationship('ReturnActions', primaryjoin='ReturnLineFlags.return_action == ReturnActions.action_id', backref='return_line_flagss')



class ReturnLineFlagsLog(db.Model):
    __tablename__ = 'return_line_flags_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, nullable=False)
    column_name = db.Column(db.Unicode(128), nullable=False)
    old_value = db.Column(db.Unicode)
    new_value = db.Column(db.Unicode)
    user = db.Column(db.Unicode(128), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.FetchedValue())



class ReturnProcessLevel(db.Model):
    __tablename__ = 'return_process_level'
    __bind_key__ = 'ordersDB'

    process_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))



class ReturnStatus(db.Model):
    __tablename__ = 'return_status'
    __bind_key__ = 'ordersDB'

    status = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(512))



class ReturnsToReplacements(db.Model):
    __tablename__ = 'returns_to_replacements'
    __bind_key__ = 'ordersDB'

    replacement_id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, nullable=False)
    replacement_sku = db.Column(db.String(159), nullable=False)
    replacement_qty = db.Column(db.Integer, nullable=False)
    replacement_guid_line = db.Column(db.Unicode(40))



class ReturnsToReplacementsLog(db.Model):
    __tablename__ = 'returns_to_replacements_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = db.Column(db.Integer, primary_key=True)
    replacement_id = db.Column(db.Integer, nullable=False)
    return_id = db.Column(db.Integer, nullable=False)
    column_name = db.Column(db.Unicode(128), nullable=False)
    old_value = db.Column(db.Unicode(128))
    new_value = db.Column(db.Unicode(128))
    user = db.Column(db.Unicode(128), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.FetchedValue())



class SalesChannel(db.Model):
    __tablename__ = 'sales_channel'
    __bind_key__ = 'ordersDB'

    sales_channel = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(100), nullable=False, unique=True)
    abbr = db.Column(db.Unicode(10), unique=True)
    service_id = db.Column(db.Unicode(50), unique=True)
    balanceable = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    enabled = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())
    product_alias_group = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_cross_insert = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())



class SalesOrderSubmissions(db.Model):
    __tablename__ = 'sales_order_submissions'
    __bind_key__ = 'ordersDB'

    so_submission_id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.Unicode(100), nullable=False)
    submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    failed_submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    last_submission_date = db.Column(db.DateTime)
    last_submission_id = db.Column(db.Unicode(100))
    sales_channel = db.Column(db.Integer, nullable=False)



class ScanLogWorkingLocations(db.Model):
    __tablename__ = 'scan_log_working_locations'
    __bind_key__ = 'ordersDB'

    UPC = db.Column(db.String(25), nullable=False, primary_key=True)
    Qty = db.Column(db.Integer, nullable=False)
    Old_Qty = db.Column(db.Integer)
    location = db.Column(db.String(30))
    date_scanned = db.Column(db.DateTime, nullable=False)
    old_location = db.Column(db.String(30))
    new_lID = db.Column(db.BigInteger)
    old_lID = db.Column(db.BigInteger)



class ShipFlags(db.Model):
    __tablename__ = 'ship_flags'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(40))
    promise_date = db.Column(db.DateTime)
    id = db.Column(db.BigInteger, primary_key=True)



class ShipmentLineSubmissions(db.Model):
    __tablename__ = 'shipment_line_submissions'
    __bind_key__ = 'ordersDB'

    shipment_line_id = db.Column(db.BigInteger, nullable=False)
    shipment_submission_id = db.Column(db.BigInteger, primary_key=True)
    sales_channel = db.Column(db.Integer, nullable=False)
    submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    failed_submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    order_id = db.Column(db.Unicode(100))
    order_line_id = db.Column(db.Unicode(120))
    last_submission_date = db.Column(db.DateTime)



class ShipmentLines(db.Model):
    __tablename__ = 'shipment_lines'
    __bind_key__ = 'ordersDB'

    shipment_line_id = db.Column(db.BigInteger, primary_key=True)
    shipment_line_status = db.Column(db.Integer, nullable=False)
    shipment_line_type = db.Column(db.Integer, nullable=False)
    tracking_number = db.Column(db.Unicode(128))
    service_level = db.Column(db.Unicode(128))
    weight = db.Column(db.Float(53))
    package_count = db.Column(db.Integer, server_default=db.FetchedValue())
    ship_timestamp = db.Column(db.DateTime, nullable=False)
    promise_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    guid_order_line = db.Column(db.ForeignKey('order_lines.guid_order_line'), nullable=False)
    carrier = db.Column(db.Integer)

    order_lines = db.relationship('OrderLines', primaryjoin='ShipmentLines.guid_order_line == OrderLines.guid_order_line')



class ShipmentLinesLog(db.Model):
    __tablename__ = 'shipment_lines_log'
    __bind_key__ = 'ordersDB'

    log_entry_id = db.Column(db.BigInteger, primary_key=True)
    guid_order_line = db.Column(db.Unicode(40), nullable=False)
    old_shipment = db.Column(db.Text)
    new_shipment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.Unicode(128))



class Shipments(db.Model):
    __tablename__ = 'shipments'
    __bind_key__ = 'ordersDB'

    guid_order_line = db.Column(db.Unicode(40), nullable=False)
    carrier = db.Column(db.Integer)
    tracking_number = db.Column(db.Unicode(128))
    service_level = db.Column(db.Unicode(128))
    weight = db.Column(db.Float(53))
    package_count = db.Column(db.Integer)
    ship_timestamp = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    Created = db.Column(db.DateTime, server_default=db.FetchedValue())
    submission_count = db.Column(db.Integer, server_default=db.FetchedValue())
    failed = db.Column(db.BIT, server_default=db.FetchedValue())
    promise_date = db.Column(db.DateTime)



class ShippingRules(db.Model):
    __tablename__ = 'shipping_rules'
    __bind_key__ = 'ordersDB'

    supplier = db.Column(db.Unicode(100))
    edi = db.Column(db.BIT)
    apo = db.Column(db.BIT)
    non_48 = db.Column(db.BIT)
    warehouse_shipment = db.Column(db.BIT)
    tranship_brand = db.Column(db.BIT)
    email_brand = db.Column(db.BIT)
    dropship_fee = db.Column(db.Unicode(10))
    restocking_fee = db.Column(db.Unicode(10))
    leadtime = db.Column(db.Unicode(8))
    brand = db.Column(db.String(41))
    id = db.Column(db.BigInteger, primary_key=True)
    po_override = db.Column(db.Unicode(10))
    valid_sales_channels = db.Column(db.Text)
    normalized_brand = db.Column(db.String(8000), server_default=db.FetchedValue())
    normalized_supplier = db.Column(db.Unicode(4000), server_default=db.FetchedValue())
    fulfillment_warehouses = db.Column(db.Text)



class SpecialOrderPo(db.Model):
    __tablename__ = 'special_order_po'
    __bind_key__ = 'ordersDB'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(199))
    date_processed = db.Column(db.DateTime)
    order_session = db.Column(db.String(199))
    sPO = db.Column(db.String(207))
    bekir_sPO = db.Column(db.String(209))
    short_sPO = db.Column(db.String(209))
    numericPO = db.Column(db.Integer)
    scanned_in = db.Column(db.String(199))
    sku = db.Column(db.String(128))
    Merchant_Order_Id = db.Column(db.Integer)
    scanned_in_date = db.Column(db.DateTime)
    numeric_po = db.Column(db.Integer)
    scan_out_by = db.Column(db.String(199))
    quantity_purchased = db.Column(db.Integer)
    purchase_date = db.Column(db.DATETIMEOFFSET)
    EDI = db.Column(db.String(50))
    order_id = db.Column(db.Unicode(128))
    order_item_id = db.Column(db.Unicode(128))
    guid_order_line = db.Column(db.Unicode(40), server_default=db.FetchedValue())



class TbProduct(db.Model):
    __tablename__ = 'tbProduct'
    __bind_key__ = 'productsDB'

    ProductID = db.Column(db.Unicode(128), nullable=False, primary_key=True)
    upc = db.Column(db.String(32))
    _Vendor = db.Column(db.Unicode(64))
    _supplier = db.Column(db.Unicode(64))
    _product_name = db.Column(db.Unicode(128))
    _shortUPC = db.Column(db.String(10))
    description = db.Column(db.Unicode)
    _cost = db.Column(db.Numeric(18, 2))
    GUIDProduct = db.Column(db.String(40))
    color = db.Column(db.Unicode(100))
    size = db.Column(db.String(64))
    ProductType = db.Column(db.String(16))
    gender = db.Column(db.String(64))
    _altSKU = db.Column(db.Unicode(128))
    normalized_brand = db.Column(db.Unicode(64))
    normalized_supplier = db.Column(db.Unicode(64))
    normalized_sku = db.Column(db.String(159))



class TbProductPricing(db.Model):
    __tablename__ = 'tbProductPricing'
    __bind_key__ = 'productsDB'

    upc = db.Column(db.String(32), primary_key=True)
    price = db.Column(db.Numeric(18,2))
    cost = db.Column(db.Numeric(18,2), nullable=False)



class TbProducts(db.Model):
    __tablename__ = 'tbProducts'
    __bind_key__ = 'productsDB'

    sku = db.Column(db.Unicode(128), primary_key=True)
    upc = db.Column(db.String(32))
    brand = db.Column(db.Unicode(64))
    supplier = db.Column(db.Unicode(64))
    gender = db.Column(db.String(64))
    product_name = db.Column(db.Unicode(128))
    product_type = db.Column(db.String(16))
    checksum = db.Column(db.BigInteger)
    google_category = db.Column(db.Unicode(256))
    _shortUPC = db.Column(db.String(10), server_default=db.FetchedValue())
    description = db.Column(db.Unicode)
    size = db.Column(db.String(64))
    GUIDProduct = db.Column(db.String(40))
    GUIDVendor = db.Column(db.String(40))
    alt_sku = db.Column(db.Unicode(128))
    normalized_brand = db.Column(db.Unicode(64), server_default=db.FetchedValue())
    normalized_supplier = db.Column(db.Unicode(64), server_default=db.FetchedValue())
    color = db.Column(db.Unicode(100))
    normalized_sku = db.Column(db.String(159), server_default=db.FetchedValue())
    last_updated = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    product_pricing = db.relationship('TbProductPricing', primaryjoin='foreign(TbProducts.upc) == remote(TbProductPricing.upc)')
    shipping_rules = db.relationship('ShippingRules',
            primaryjoin='(foreign(TbProducts.brand) == remote(ShippingRules.brand)) and (foreign(TbProducts.supplier) == remote(ShippingRules.supplier))')

class TbVendor(db.Model):
    __tablename__ = 'tbVendor'
    __bind_key__ = 'productsDB'

    vendor = db.Column(db.Unicode(64), primary_key=True)
    GUIDVendor = db.Column(db.String(40))



class TblInvLocations(db.Model):
    __tablename__ = 'tblInvLocations'
    __bind_key__ = 'inventoryDB'

    lID = db.Column(db.BigInteger, primary_key=True)
    Row = db.Column(db.String(10), nullable=False)
    Level = db.Column(db.String(10), nullable=False)
    Col = db.Column(db.String(10), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    rev = db.Column(db.String(50))
    UPC = db.Column(db.String(25))
    guidItemLoc = db.Column(db.Integer, server_default=db.FetchedValue())
    shortUPC = db.Column(db.String(10), server_default=db.FetchedValue())
    lastModTime = db.Column(db.DateTime, server_default=db.FetchedValue())
    QTY_Avail = db.Column(db.Integer)



class VInvLocationsDev(db.Model):
    __tablename__ = 'vInvLocationsDev'
    __bind_key__ = 'inventoryDB'

    Row = db.Column(db.String(10), nullable=False, primary_key=True)
    Level = db.Column(db.String(10), nullable=False)
    Col = db.Column(db.String(10), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    UPC = db.Column(db.String(25))
    lID = db.Column(db.BigInteger, nullable=False)
    rev = db.Column(db.String(50))
    SKU = db.Column(db.Unicode(4000))
    imageURL = db.Column(db.Unicode(4000))
    shortUPC = db.Column(db.String(10))
    location = db.Column(db.String(30), nullable=False)
    QTY_Avail = db.Column(db.Integer)
    sku_seg = db.Column(db.Unicode(4000))



class VProductUrls(db.Model):
    __tablename__ = 'vProductUrls'
    __bind_key__ = 'inventoryDB'

    UPC = db.Column(db.String(32), primary_key=True)
    _shortUPC = db.Column(db.String(10))
    imageURL = db.Column(db.Unicode(4000))



class VReturnsDetails(db.Model):
    __tablename__ = 'vReturns_Details'
    __bind_key__ = 'ordersDB'

    return_line_id = db.Column(db.BigInteger, nullable=False)
    replacement_so_number = db.Column(db.Unicode(128))
    replacement_po_number = db.Column(db.Unicode(128))
    returns_status = db.Column(db.Unicode(512))
    order_id = db.Column(db.Unicode(100))
    order_line_id = db.Column(db.Unicode(120))
    package_condition = db.Column(db.Unicode(512))
    product_condition = db.Column(db.Unicode(512))
    returns_action = db.Column(db.Unicode(512))
    notes = db.Column(db.Unicode)
    replacement_sku = db.Column(db.Unicode(128))
    created = db.Column(db.DateTime)
    guid_order_line = db.Column(db.Unicode(40), nullable=False, primary_key=True)
    sku = db.Column(db.String(159))
    qty_ordered = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime)
    sales_channel = db.Column(db.Integer)
    sales_order_number = db.Column(db.Integer)
    ship_name = db.Column(db.Unicode(500))
    ship_phone = db.Column(db.Unicode(100))
    ship_address_1 = db.Column(db.Unicode(500))
    ship_address_2 = db.Column(db.Unicode(500))
    ship_address_3 = db.Column(db.Unicode(500))
    ship_city = db.Column(db.Unicode(500))
    ship_state = db.Column(db.Unicode(500))
    ship_postal_code = db.Column(db.Unicode(100))
    ship_country = db.Column(db.Unicode(500))
    replacement_order_id = db.Column(db.Unicode(128))
    replacement_GUID_order_line = db.Column(db.Unicode(40))
    tracking_number = db.Column(db.Unicode(128))
    ship_timestamp = db.Column(db.DateTime)



class Warehouses(db.Model):
    __tablename__ = 'warehouses'
    __bind_key__ = 'ordersDB'

    warehouse_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    abbr = db.Column(db.String(10), nullable=False)
    enabled = db.Column(db.BIT, nullable=False, server_default=db.FetchedValue())



class ZipCities(db.Model):
    __tablename__ = 'zip_cities'
    __bind_key__ = 'ordersDB'

    zip_code = db.Column(db.String(25), primary_key=True)
    zip_cities = db.Column(db.Unicode, nullable=False)



class ZipCodes(db.Model):
    __tablename__ = 'zip_codes'
    __bind_key__ = 'ordersDB'

    zip_code = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(5), nullable=False)
    id = db.Column(db.BigInteger, primary_key=True)
