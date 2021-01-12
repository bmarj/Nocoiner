from wtforms_components import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError
# from flask_wtf import FlaskForm
from api.models import combined as m
from api.models.form_base import ModelForm

class InventoryForm(ModelForm):
    class Meta:
        model = m.TblInvLocations
        include = ['Row', 'Level', 'Qty', 'UPC']
        exclude = ['guidItemLoc', 'lastModTime', 'shortUPC', 'QTY_Avail', 'rev']
    # submit = SubmitField('Submit')


# class ChangeQuantityForm(ModelForm):
#     class Meta:
#         model = m.TblInvLocations
#         include = ['Qty']
#         exclude = ['guidItemLoc', 'lastModTime', 'shortUPC', 'QTY_Avail', 'rev', 'Row', 'Level', 'UPC']

class ChangeQuantityForm(ModelForm):
    class Meta:
        model = m.TblInvLocations
        include = ['Row', 'Level', 'Qty', 'UPC']
        exclude = ['guidItemLoc', 'lastModTime', 'shortUPC', 'QTY_Avail', 'rev']
    UpdatedQty = IntegerField("Quantity", validators=[DataRequired("New quantity is required")])

    def validate_UpdatedQty(self, field):
        if field.data <= 0:            
            raise ValidationError("Value must be greater than zero.")
        if field.data > 10000:
            raise ValidationError("Too many items to add for manual change (just for demo).")