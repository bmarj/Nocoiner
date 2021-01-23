from wtforms_components import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError
# from flask_wtf import FlaskForm
from api import models as m
from api.models.form_base import ModelForm, FormMeta

class OrderForm(ModelForm):
    class Meta(FormMeta):
        model = m.Order
        only = ['order_number', 'ship_name', 'ship_phone', 'ship_email', 
        'ship_address', 'ship_address_2', 'ship_city', 
        'ship_postal_code', 'ship_country', 'ship_state']
        # set/override labels manually
        # field_args = {'ship_country': {'label': 'Country'} }
