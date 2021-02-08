def titlecase_label(fieldname):
    if '_' in fieldname or fieldname == fieldname.lower():
        return ' '.join([w.title() for w in fieldname.split('_') if w != 'id'])
    return fieldname

def ends_with_dot(text):
    if not text.endswith("."):
        return text + "."
    return text

def init_app(app):
  """Initialize a Flask application with custom filters."""
  app.jinja_env.filters['titlecase_label'] = titlecase_label
  app.jinja_env.filters['end_dot'] = ends_with_dot