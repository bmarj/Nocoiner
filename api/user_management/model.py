# coding: utf-8
import datetime
from flask import g
from api.models.model_base import db, BIT, DECIMAL, NUMERIC, DATETIMEOFFSET, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship


class User(db.Model):
    __tablename__ = "app_user"
    __bind_key__ = 'ordersDB'
    
    id = db.Column(db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean)
    email = db.Column(db.String(64), unique=True, nullable=False)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer)
    fail_login_count = db.Column(db.Integer)
    #roles = db.relationship("Role", secondary=assoc_user_role, backref="user")
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)

    # @declared_attr
    # def created_by_fk(self):
    #     return db.Column(
    #         db.Integer, db.ForeignKey("user.id"), default=self.get_user_id, nullable=True
    #     )

    # @declared_attr
    # def changed_by_fk(self):
    #     return db.Column(
    #         db.Integer, db.ForeignKey("user.id"), default=self.get_user_id, nullable=True
    #     )

    # created_by = db.relationship(
    #     "User",
    #     backref=db.backref("created", uselist=True),
    #     remote_side=[id],
    #     primaryjoin="User.created_by_fk == User.id",
    #     uselist=False,
    # )
    # changed_by = db.relationship(
    #     "User",
    #     backref=db.backref("changed", uselist=True),
    #     remote_side=[id],
    #     primaryjoin="User.changed_by_fk == User.id",
    #     uselist=False,
    # )

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return self.get_full_name()


# class Role(db.Model):
#     __tablename__ = "role"
#     __bind_key__ = 'ordersDB'

#     id = db.Column(db.Integer, db.Sequence("role_id_seq"), primary_key=True)
#     name = db.Column(db.String(64), unique=True, nullable=False)
#     permissions = db.relationship(
#         "PermissionView", secondary=assoc_permissionview_role, backref="role"
#     )

#     def __repr__(self):
#         return self.name


# class Permission(db.Model):
#     __tablename__ = "permission"
#     __bind_key__ = 'ordersDB'
#     id = db.Column(db.Integer, db.Sequence("permission_id_seq"), primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)

#     def __repr__(self):
#         return self.name

