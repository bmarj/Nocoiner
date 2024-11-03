from flask_wtf import FlaskForm
from sqlalchemy.sql.expression import label
from wtforms_components import DateField
from wtforms.meta import DefaultMeta
from datetime import datetime
from wtforms_sqlalchemy.orm import model_form, ModelConverter, converts
from wtforms import fields as wtforms_fields
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package
from .model_base import db
from .custom_widgets import BootstrapCheckboxInput


class CustonModelConverter(ModelConverter):
    @converts("Boolean", "dialects.mssql.base.BIT")
    def conv_Boolean(self, field_args, **extra):
        return wtforms_fields.BooleanField(widget=BootstrapCheckboxInput(), **field_args)


class FormMeta(DefaultMeta):
    """ Binds application default widgets. You can override widget at field level. 
    """
    def bind_field(self, form, unbound_field, options):
        bound = super().bind_field(form, unbound_field, options)
        if bound.type == "BooleanField":
            bound.widget = BootstrapCheckboxInput()
        return bound
    
    model = None
    base_class = FlaskForm
    only = None
    exclude = ['created_by', 'changed_by', 'created_on', 'changed_on',]
    field_args = None
    converter = CustonModelConverter()
    exclude_pk = True
    exclude_fk = True
    type_name = None

    # def render_field(self, field, render_kw):
    #     render_kw['class'] = 'form-control ' + render_kw.get('class', '')
    #     return super().render_field(field, render_kw)


class ModelForm(FlaskForm):
    class Meta(FormMeta):
        pass
    # execute code when subclassing:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        newcls =  model_form(cls.Meta.model, 
                             db.session, 
                             base_class=FlaskForm,
                             only=cls.Meta.only, 
                             exclude=cls.Meta.exclude, 
                             field_args=cls.Meta.field_args, 
                             converter=cls.Meta.converter, 
                             exclude_pk=cls.Meta.exclude_pk, 
                             exclude_fk=cls.Meta.exclude_fk, 
                             type_name=cls.Meta.type_name)
        # set model attribute to the form
        newcls.Meta.model = cls.Meta.model
        cls.form = newcls

def create_model_form(model, base_class=FlaskForm, only=None, exclude=None, field_args=None, converter=None, exclude_pk=True, exclude_fk=True, type_name=None):
    # use model_form to create a form
    form =  model_form(model, db.session, base_class=base_class, only=only, exclude=exclude, field_args=field_args, converter=converter or CustonModelConverter(), exclude_pk=exclude_pk, exclude_fk=exclude_fk, type_name=type_name)
    form.Meta.model = model
    return form

# from https://stackoverflow.com/questions/27766417/how-to-implement-not-required-datefield-using-flask-wtf?rq=1
class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))