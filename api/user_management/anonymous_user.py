# coding: utf-8
from flask_login import AnonymousUserMixin
from .model import Role, Permission

class AnonymousUser(AnonymousUserMixin):

    def get_full_name(self):
        return "Guest"

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
        anonymous user permissions
        """
        q = [Permission(name="guest"), Permission(name="anonymous")]
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
        anonymous user role
        """
        q = [Role(name="guest"),Role(name="anonymous")]
        return q