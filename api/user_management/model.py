# coding: utf-8
import datetime
from flask import g
from werkzeug.security import generate_password_hash
from api.models.model_base import db, BIT, DECIMAL, NUMERIC, DATETIMEOFFSET, MetaData
#from sqlalchemy import Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, column_property, relationship


class DefaultMeta(MetaData):
    __bind_key__ = 'ordersDB'


class Role(db.Model):
    __tablename__ = "role"
    __bind_key__ = 'ordersDB'

    id = db.Column(db.Integer, db.Sequence("role_id_seq"), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    #permissions = db.relationship("Permission")
    #role_permissions = db.relationship("RolePermission", uselist=True)

    def __repr__(self):
        return self.name


class Permission(db.Model):
    __tablename__ = "permission"
    __bind_key__ = 'ordersDB'
    id = db.Column(db.Integer, db.Sequence("permission_id_seq"), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name


# assoc_user_role = Table(
#     "app_user_role",
#     DefaultMeta,
#     id = db.Column(db.Integer, db.Sequence("user_role_id_seq"), primary_key=True),
#     app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id")),
#     role_id = db.Column(db.Integer, db.ForeignKey("role.id")),
#     #db.UniqueConstraint("user_id", "role_id")
# )

class RolePermission(db.Model):
    __tablename__ = "role_permission"
    __bind_key__ = 'ordersDB'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    permission_id = db.Column(db.Integer, db.ForeignKey("permission.id"))

    role = db.relationship(
        "Role",
        backref=backref("role_permissions", uselist=True)
    )
    permission = db.relationship(
        "Permission", 
        backref=backref("role_permissions", uselist=True)
    )


class UserRole(db.Model):
    __tablename__ = "app_user_role"
    __bind_key__ = 'ordersDB'

    id = db.Column(db.Integer, primary_key=True)
    app_user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    #db.UniqueConstraint("user_id", "role_id")
    user = db.relationship(
        "User",
        backref=backref("user_roles", uselist=True)
    )
    role = db.relationship(
        "Role",
        backref=backref("user_roles", uselist=True)
    )


class User(db.Model):
    __tablename__ = "app_user"
    __bind_key__ = 'ordersDB'
    
    id = db.Column(db.Integer, db.Sequence("app_user_id_seq"), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256))
    active = db.Column(db.Boolean)
    email = db.Column(db.String(64), unique=True, nullable=False)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer)
    fail_login_count = db.Column(db.Integer)

    # user_roles = db.relationship("UserRole")

    #primaryjoin='(User.id == UserRole.app_user_id) and (UserRole.role_id == Role.id)'

    # permissions = db.relationship("Permission", 
    #     primaryjoin='(User.id == UserRole.app_user_id) AND (UserRole.role_id == Role.id) AND (Role.id == RolePermisssion.role_id) AND (RolePermission.permission_id == Permission.id)'
    # )

    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)

    # full_name = column_property(first_name + " " + last_name)

    @property
    def plain_password(self):
        return None

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    @declared_attr
    def created_by_id(self):
        return db.Column(
            db.Integer, db.ForeignKey("app_user.id"), default=self.get_user_id, nullable=True
        )

    @declared_attr
    def changed_by_id(self):
        return db.Column(
            db.Integer, db.ForeignKey("app_user.id"), default=self.get_user_id, nullable=True
        )

    created_by = db.relationship(
        "User",
        backref=db.backref("created", uselist=True),
        remote_side=[id],
        primaryjoin="User.created_by_id == User.id",
        uselist=False
    )
    changed_by = db.relationship(
        "User",
        backref=db.backref("changed", uselist=True),
        remote_side=[id],
        primaryjoin="User.changed_by_id == User.id",
        uselist=False
    )

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

    def has_role(self, role: str) -> bool:
        return role.lower() in self.roles

    def has_permission(self, permission: str) -> bool:
        return permission.lower() in self.permissions

    def any_role(self, *role: str) -> bool:
        for r in role:
            if r.lower() in self.roles:
                return True
        return False

    def any_permission(self, *permission: str) -> bool:
        for p in permission:
            if p.lower() in self.permissions:
                return True
        return False

    _permissions = None
    @property
    def permissions(self) -> dict:
        """
        Use this dict to check authorization.
        Once accesssed, it will cache roles for the lifetime of an object
        """
        if not self._permissions:
            self._permissions = {p.name.lower(): p for p in self.get_permissions()}
        return self._permissions

    def get_permissions(self):
        """
        get user permissions from database
        """
        q = Permission.query\
            .join(RolePermission)\
            .join(Role)\
            .join(UserRole)\
            .filter(UserRole.app_user_id == int(self.id))\
            .all()
        return q

    _roles = None
    @property
    def roles(self) -> dict:
        """
        Use this dict to check authorization.
        Once accesssed, it will cache roles for the lifetime of an object
        """
        if not self._roles:
            self._roles = {p.name.lower(): p for p in self.get_roles()}
        return self._roles

    def get_roles(self):
        """
        get user roles from database
        """
        q = Role.query\
            .join(UserRole)\
            .filter(UserRole.app_user_id == int(self.id))\
            .all()
        return q

    def __repr__(self):
        return self.get_full_name()


