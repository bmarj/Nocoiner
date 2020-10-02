from marshmallow import pre_load, post_load, post_dump, Schema
from marshmallow.utils import get_value, set_value
from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import (
    SQLAlchemyAutoSchema, SQLAlchemySchema, SQLAlchemyAutoSchemaOpts)
from api.models import db


class BasicMeta:
    """
    with session.
    session is needed for deserialization
    """
    sqla_session = db.session


class SimpleMeta(BasicMeta):
    """
    Simple table schema rules, no related data loading
    """
    # default serialization options
    include_relationships = False
    include_fk = False
    load_instance = True


class NamespaceOpts(SQLAlchemyAutoSchemaOpts):
    """Same as the default class Meta options, but adds "name" and
    "plural_name" options for enveloping.
    """

    def __init__(self, meta, **kwargs):
        SQLAlchemyAutoSchemaOpts.__init__(self, meta, **kwargs)
        self.name = getattr(meta, "name", None)
        self.plural_name = getattr(meta, "plural_name", self.name)


class NamespacedSchema(SQLAlchemyAutoSchema):
    '''
    # example:

    class OrderFeedsSchema(NamespacedSchema):
        class Meta(BasicMeta):
            name = "order_line"
            plural_name = "order_line"
    '''
    OPTIONS_CLASS = NamespaceOpts

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}


class AliasedFieldsSchema(SQLAlchemyAutoSchema):
    """
    Enumerate related fields in Meta class like:
    fields = ('order.order_id')
    options:
    field_alias_dict = {}
    auto_flatten_fields = True
    Use field_alias_dict to map fields from one namespace to another or root.     
    Use auto_flatten_fields=True and fields will be serialized in the same namespace as root.
    If field_alias_dict is used with auto_flatten_fields, only fields without alias are flattened.
    """

    field_alias_dict = {}
    auto_flatten_fields = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for k, v in OrderSchema._declared_fields.items():
    #         self._declared_fields.update({'order.' + k: v})

    def on_bind_field(self, field_name, field_obj):
        if self.field_alias_dict and self.field_alias_dict.get(field_name):
            mapped_name = self.field_alias_dict.get(field_name)
            if self.declared_fields.get(mapped_name):
                raise Exception("Field already exists. Alias: '"
                                + mapped_name
                                + "' for field '" + field_name + "'")
            field_obj.data_key = mapped_name
        elif self.auto_flatten_fields and '.' in field_name:
            parts = field_name.split('.')
            prop_name = parts[len(parts) - 1]
            if self.declared_fields.get(prop_name):
                raise Exception("Field already exists. Alias: '"
                                + prop_name
                                + "' for field '" + field_name + "'")
            field_obj.data_key = prop_name

    # def get_translated(self, data, **kwargs):
    #     temp = self.load(data, **kwargs)
    #     return self.load(self.dump(temp), **kwargs)


class Reach(fields.Field):
    '''
    Custom field type, for nested objects
    # example:

    class User(Schema):
        name = fields.String()
        title = Reach(fields.Str(), data_key="book", path="title")
    '''

    def __init__(self, inner, path, **kwargs):
        super().__init__(**kwargs)
        self.inner = inner
        self.path = path

    def _deserialize(self, value, attr, data, **kwargs):
        val = get_value(value, self.path)
        return self.inner.deserialize(val, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        val = self.inner._serialize(value, attr, obj, **kwargs)
        ret = {}
        set_value(ret, self.path, val)
        return ret
