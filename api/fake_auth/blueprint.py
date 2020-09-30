from flask import Blueprint, session, jsonify, make_response
import json

auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static', static_url_path='/static')


@auth.route('/login', methods=['POST'])
def login():
    return '', 200

@auth.route('/logout', methods=['GET'])
def logout():
    return 'OK', 200

@auth.route('/auth_test', methods=['GET'])
def get_auth_info():
    return make_response(
        json.dumps(
            {"auth": [{"apps": [{"app_name": "Pick Ticket Scanout", "app_url": "../pick_ticket_scan/scan_out.html", "apps_icon": "../resources/images/barcode.png"}, {"app_name": "Special Order Scan In", "app_url": "../special_order_checkin/checkin.html", "apps_icon": "../resources/images/barcode.png"}, {"app_name": "Live Inventory", "app_url": "../Inventory/Inventory.html", "apps_icon": "../resources/images/box.png"}, {"app_name": "Inventory Move", "app_url": "../inventory_move/inventory_move.html", "apps_icon": "../resources/images/box.png"}, {"app_name": "Scan to Shipping", "app_url": "../inventory_to_shipping/inventory_to_shipping.html", "apps_icon": "../resources/images/box.png"}, {"app_name": "Inventory Label Generator", "app_url": "../inventory_label_generator/inventory_label_generator.html", "apps_icon": "../resources/images/box.png"}, {"app_name": "Add Order", "app_url": "../add_order/add_order.html", "apps_icon": "../resources/images/cart.png"}, {"app_name": "Order Export", "app_url": "../order_exporter/exporter.html", "apps_icon": "../resources/images/export.png"}, {"app_name": "Order Line View", "app_url": "../order_line_view/order_lines.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Sales Reports", "app_url": "../sales_report/sales_report.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Special Order Reports", "app_url": "../special_order_feed/special_order_report.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Shipping Rules Editor", "app_url": "../shipping_rules_editor/index.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Return View", "app_url": "../returns/returns.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "ASIN Interface", "app_url": "../asin/interface.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Bulk Mark Ship", "app_url": "../bulk_mark_ship/index.html", "apps_icon": "../resources/images/table.png"}, {"app_name": "Sales Channel Editor", "app_url": "../sales_channel_editor/sales_channels.html", "apps_icon": "../resources/images/table.png"}], "authorized": 1, "last_attempt": 5999940651.037, "authorized_on": 0, "expires": "2020-12-08T02:52:27", "username": "bmarjanovic", "groups": ["OfficeUsers", "WorldblitzSuiteUsers", "Developers", "orderWriters", "WorldBlitzOffice", "vpn_users", "CommerceBlitz Admins", "orderExporters"]}]}
        ),
        {'Content-Type': 'application/json'}
    )
