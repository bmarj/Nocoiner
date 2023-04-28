from marshmallow_sqlalchemy import fields
from wtforms_components import StringField, IntegerField
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from wtforms_alchemy import QuerySelectField
from flask_wtf import FlaskForm
from api.models.form_base import ModelForm, FormMeta
from .business import query_permissions, query_roles, query_users
from . import model as m


class LoginForm(FlaskForm):
    # class Meta(FormMeta):
    #     model = m.User
    #     only = ['username', 'password']
    #     # set/override labels manually
    #     #field_args = {'ship_country': {'label': 'Country'} }
    username = StringField(validators=[DataRequired("Please enter username")])
    password = PasswordField(validators=[DataRequired("Please enter password")])
    remember_me = BooleanField()


class RoleForm(ModelForm):
    class Meta(FormMeta):
        model = m.Role

class PermissionForm(ModelForm):
    class Meta(FormMeta):
        model = m.Permission
        only = ['name']

class UserRoleForm(ModelForm):
    class Meta(FormMeta):
        model = m.UserRole

    # map it to name of model relation
    user = QuerySelectField(
        label="User",
        query_factory=lambda: query_users().all(),
        allow_blank=True, blank_text='-- Empty --',
        validators=[DataRequired()],
        get_label=lambda a: a.first_name + ' ' + a.last_name)

    # map it to name of model relation
    role = QuerySelectField(
        label="Role",
        query_factory=lambda: query_roles().all(),
        allow_blank=True, blank_text='-- Empty --',
        validators=[DataRequired()],
        get_label=lambda a: a.name)

class RolePermissionForm(ModelForm):
    class Meta(FormMeta):
        model = m.RolePermission

    # map it to name of model relation
    role = QuerySelectField(
        label="Role",
        query_factory=lambda: query_roles().all(),
        allow_blank=True, blank_text='-- Empty --',
        validators=[DataRequired()],
        get_label=lambda a: a.name)

    # map it to name of model relation
    permission = QuerySelectField(
        label="Permission",
        query_factory=lambda: query_permissions().all(),
        allow_blank=True, blank_text='-- Empty --',
        validators=[DataRequired()],
        get_label=lambda a: a.name)

class UserForm(ModelForm):
    class Meta(FormMeta):
        model = m.User
        exclude = ['password']
    plain_password = PasswordField('Password')