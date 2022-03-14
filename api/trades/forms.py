from wtforms_components import StringField, IntegerField
from wtforms import BooleanField
from wtforms.validators import DataRequired, ValidationError
# from flask_wtf import FlaskForm
from api import models as m
from api.models.form_base import ModelForm, FormMeta

class TradeForm(ModelForm):
    class Meta(FormMeta):
        model = m.Trade
        only = ['symbol']
        # set/override labels manually
        # field_args = {'symbol': {'label': 'Symbol'} }

class LeaderForm(ModelForm):
    class Meta(FormMeta):
        model = m.Leader
        only = ['name', 'encrypted_uid', 'is_active']
        # set/override labels manually
        # field_args = {'symbol': {'label': 'Symbol'} }
    is_active = BooleanField()
