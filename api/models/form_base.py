from flask_wtf import FlaskForm
from sqlalchemy.sql.expression import label
from wtforms_components import DateField
from wtforms.meta import DefaultMeta
from datetime import datetime
from wtforms_alchemy import model_form_factory
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package
from .model_base import db

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class FormMeta(DefaultMeta):
    pass
    # def render_field(self, field, render_kw):
    #     render_kw['class'] = 'form-control ' + render_kw.get('class', '')
    #     return super().render_field(field, render_kw)


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