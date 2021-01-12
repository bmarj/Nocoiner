from wtforms import StringField, TextField, SubmitField
from api.models import combined as m
from api.models.form_base import ModelForm

class InventoryForm(ModelForm):
    class Meta:
        model = m.TblInvLocations
        include = ['Row', 'Level', 'Qty', 'UPC']
        exclude = ['Col', 'guidItemLoc', 'lastModTime', 'shortUPC', 'QTY_Avail', 'rev']
    # submit = SubmitField('Submit')
