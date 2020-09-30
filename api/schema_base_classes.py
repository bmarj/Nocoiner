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
