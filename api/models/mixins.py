import datetime
#import sqlalchemy as sa
from api.models.model_base import db, BIT, DECIMAL, NUMERIC, DATETIMEOFFSET, MetaData
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from flask import session


# TODO: ensure user can't override values, using before_flush or aproach from link
#      https://stackoverflow.com/questions/17410315/onupdate-not-overridinig-current-datetime-value
# @as_declarative()
class AuditMixin(db.Model):
    """Mixin that define create/change audit."""

    __abstract__ = True

    __datetime_func__ = lambda: datetime.datetime.now()
    __identity_func__ = lambda: session['_user_id']

    created_on = db.Column(db.DateTime(),
                           default=__datetime_func__,
                           nullable=False)

    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer(),
                         db.ForeignKey("app_user.id"),
                         default=lambda: session['_user_id'],
                         onupdate=lambda: session['_user_id'],
                         nullable=False)

    @declared_attr
    def created_by(cls):
        return db.relationship("User",
            primaryjoin=f"User.id=={cls.__name__}.created_by_id"
        )

    changed_on = db.Column(db.DateTime(),
                           default=__datetime_func__,
                           onupdate=__datetime_func__,
                           nullable=False)

    @declared_attr
    def changed_by_id(cls):
        return db.Column(db.Integer(),
                         db.ForeignKey("app_user.id"),
                         default=lambda: session['_user_id'],
                         onupdate=lambda: session['_user_id'],
                         nullable=False)

    @declared_attr
    def changed_by(cls):
        return db.relationship("User",
            primaryjoin=f"User.id=={cls.__name__}.changed_by_id"
        )
