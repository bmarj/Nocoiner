from markupsafe import Markup
from wtforms.widgets import Input


class BootstrapCheckboxInput(Input):
    """
    Render a bootstrap checkbox.

    The ``checked`` HTML attribute is set if the field's data is a non-false value.
    """
    input_type = 'checkbox'
    validation_attrs = ["required", "disabled"]

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        html = """
        <div class="form-checkbox">
            <label>
                {cb}
                <span class="checkmark"><i class="fa fa-check"></i></span>
            </label>
        </div>""".format(cb=super().__call__(field, **kwargs), 
                         label=field.label.text.replace('_',' '))
        return Markup(html)
