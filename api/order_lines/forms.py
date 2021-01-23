from wtforms_components import StringField, IntegerField, SelectField
from wtforms_alchemy import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired, Optional
from api.models import combined as m
from api.models.form_base import ModelForm, FormMeta
from .business import query_order_line_status

class OrderLineForm(ModelForm):
    class Meta(FormMeta):
        model = m.OrderLine
        only = ['sku', 'order_line_status_id']
        # set/override labels manually
        field_args = {'sku': {'label': 'SKU'} }

    order_line_status = QuerySelectField(
        label="Status",
        query_factory=lambda: query_order_line_status().all(),
        allow_blank=True, blank_text='-- Unknown --',
        get_label=lambda a: a.description,
        validators=[Optional()])



# class ChangeQuantityForm(ModelForm):
#     class Meta:
#         model = m.TblInvLocations
#         only = ['Qty']

# class ChangeShippingForm(ModelForm):
#     class Meta:
#         model = m.TblInvLocations
#         only = ['Row', 'Level', 'Qty', 'Col', 'UPC']
#     UpdatedQty = IntegerField("Quantity to add", validators=[DataRequired("New quantity is required")])

#     def validate_UpdatedQty(self, field):
#         if field.data <= 0:            
#             raise ValidationError("Value must be greater than zero.")
#         if field.data > 10000:
#             raise ValidationError("Too many items to add for manual change (just for demo).")
