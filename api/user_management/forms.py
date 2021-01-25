from wtforms_components import StringField, IntegerField
from wtforms import PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from api import models as m
from api.models.form_base import ModelForm, FormMeta

class LoginForm(FlaskForm):
    # class Meta(FormMeta):
    #     model = m.User
    #     only = ['username', 'password']
    #     # set/override labels manually
    #     #field_args = {'ship_country': {'label': 'Country'} }
    username = StringField(validators=[DataRequired("Please enter username")])
    password = PasswordField(validators=[DataRequired("Please enter password")])
    remember_me = BooleanField()
