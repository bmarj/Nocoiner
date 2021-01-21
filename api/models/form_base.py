from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms.meta import DefaultMeta

# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package
from .model_base import db

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class FormMeta(DefaultMeta):
    
    def render_field(self, field, render_kw):
        render_kw['class'] = 'form-control ' + render_kw.get('class', '')
        return super().render_field(field, render_kw)

def title_case_label_args(columns):
    return { n: {'label': ' '.join([w.title() for w in n.split('_')])} for n in columns}
