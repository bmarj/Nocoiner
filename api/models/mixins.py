import datetime

import sqlalchemy
#import sqlalchemy as sa
from api.models.model_base import db, BIT, DECIMAL, NUMERIC, DATETIMEOFFSET, MetaData
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from flask import session


# Ensure user can't override values, using before_flush or aproach from link
#   https://stackoverflow.com/questions/17410315/onupdate-not-overridinig-current-datetime-value
# currently implemented based on https://stackoverflow.com/a/12754068
class AuditMixin(db.Model):
    """Mixin that define create/change audit.
       Call ModelClass.force_audited() to ensure values are not overriden in business code.
    """
    __abstract__ = True

    __current_user_id_func = lambda: session['_user_id']
    __datetime_func__ = lambda: datetime.datetime.now()

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
            foreign_keys=cls.created_by_id)

    changed_on = db.Column(db.DateTime(),
                           default=__datetime_func__,
                           onupdate=__datetime_func__,
                           nullable=False)

    @declared_attr
    def changed_by_id(cls):
        return db.Column(db.Integer(),
                         db.ForeignKey("app_user.id"),
                         default=cls.__current_user_id_func,
                         onupdate=cls.__current_user_id_func,
                         nullable=False)

    @declared_attr
    def changed_by(cls):
        return db.relationship("User",
            foreign_keys=cls.changed_by_id)

    @staticmethod
    def ensure_insert_audit(mapper, connection, target):
        target.created_on = datetime.datetime.now()
        target.changed_on = target.created_on
        target.created_by_id = AuditMixin.__current_user_id_func()
        target.changed_by_id = AuditMixin.__current_user_id_func()

    @staticmethod
    def ensure_update_audit(mapper, connection, target):
        target.changed_on = datetime.datetime.now()
        target.changed_by_id = AuditMixin.__current_user_id_func()

    @classmethod
    def force_audited(cls):
        sqlalchemy.event.listen(cls, 'before_insert', cls.ensure_insert_audit)
        sqlalchemy.event.listen(cls, 'before_update', cls.ensure_update_audit)

