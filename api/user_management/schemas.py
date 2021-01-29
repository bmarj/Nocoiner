from marshmallow_sqlalchemy import fields, fields_for_model, auto_field
from api.models.schema_base import (
    SQLAlchemyAutoSchema, SimpleMeta, GridSimpleMeta)
from . import model as m

class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Permission
        #fields = ['description']
    #sales_channel = fields.Nested(SalesChannelSchema)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.User
        #fields = ['description']
    #sales_channel = fields.Nested(SalesChannelSchema)

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.Role
        #fields = ['description']
    #sales_channel = fields.Nested(SalesChannelSchema)

class UserRoleSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.UserRole
        #fields = ['description']
    user = fields.Nested(UserSchema)
    role = fields.Nested(RoleSchema)

class RolePermissionSchema(SQLAlchemyAutoSchema):
    class Meta(GridSimpleMeta):
        model = m.RolePermission
        #fields = ['description']
    role = fields.Nested(RoleSchema)
    permission = fields.Nested(PermissionSchema)
