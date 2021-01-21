from wtforms_components import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError
# from flask_wtf import FlaskForm
from api.models import combined as m
from api.models.form_base import ModelForm, FormMeta, title_case_label_args

class OrderLineForm(ModelForm):
    class Meta(FormMeta):
        model = m.OrderLine
        only = ['sku']
        field_args = title_case_label_args(only)
        field_args['sku'] = {'label': 'SKU'}

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