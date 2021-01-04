from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from api.models import combined as m
from api.models.schema_base_classes import SimpleMeta

ma = Marshmallow()


class AcctivateProductVendorSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.AcctivateProductVendor

class AmazonDataSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.AmazonData

class AmazonDataLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.AmazonDataLog

class BalancerActionSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.BalancerAction

class BalancerSubmissionResultSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.BalancerSubmissionResult

class CarrierSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.Carrier

class InventoryBalancerLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.InventoryBalancerLog

class InventoryBalancerSubmissionLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.InventoryBalancerSubmissionLog

class InventoryBalancerSubmissionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.InventoryBalancerSubmissions

class InventoryLocationsAvaiableSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.InventoryLocationsAvaiable

class InventoryLocationsSpecialSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.InventoryLocationsSpecial

class LinkedOrderLinesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.LinkedOrderLines

class MerchantOrderIdSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.MerchantOrderId

class OrderFlagsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderFlags

class OrderLineFlagsLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineFlagsLog

class OrderLineHierarchySchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineHierarchy

class OrderLineStatusSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineStatus

class OrderLineStatusExclusionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineStatusExclusions

class OrderLineTypeAssignmentSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineTypeAssignment

class OrderLineTypeExclusionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineTypeExclusions

class OrderLinesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLines

class OrderLineFlagsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderLineFlags

class OrderStatusSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderStatus

class OrderViewSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.OrderView

class OrdersSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.Orders

class PackageConditionSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.PackageCondition

class ProductAliasGroupsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ProductAliasGroups

class ProductConditionSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ProductCondition

class ProductCostSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ProductCost

class PullLocationSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.PullLocation

class ReturnActionSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnAction

class ReturnActionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnActions

class ReturnConditionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnConditions

class ReturnDetailsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnDetails

class ReturnLineFlagsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnLineFlags

class ReturnLineFlagsLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnLineFlagsLog


class ReturnProcessLevelSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnProcessLevel


class ReturnStatusSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnStatus


class ReturnsToReplacementsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnsToReplacements

class ReturnsToReplacementsLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ReturnsToReplacementsLog

class SalesChannelSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.SalesChannel

class SalesOrderSubmissionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.SalesOrderSubmissions

class ScanLogWorkingLocationsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ScanLogWorkingLocations

class ShipFlagsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ShipFlags

class ShipmentLineSubmissionsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ShipmentLineSubmissions

class ShipmentLinesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ShipmentLines

class ShipmentLinesLogSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ShipmentLinesLog

class ShipmentsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.Shipments

class ShippingRulesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ShippingRules

# class SpecialOrderPoSchema(SQLAlchemyAutoSchema):
#     class Meta(SimpleMeta):
#         model = m.SpecialOrderPo

class TbProductSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.TbProduct

class TbProductPricingSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.TbProductPricing

class TbProductsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.TbProducts

class TbVendorSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.TbVendor

class TblInvLocationsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.TblInvLocations

class VInvLocationsDevSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.VInvLocationsDev

class VProductUrlsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.VProductUrls

class VReturnsDetailsSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.VReturnsDetails

class WarehousesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.Warehouses

class ZipCitiesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ZipCities

class ZipCodesSchema(SQLAlchemyAutoSchema):
    class Meta(SimpleMeta):
        model = m.ZipCodes
