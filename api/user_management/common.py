from flask import request, render_template, flash


def generic_add(form, template):
    obj = form.Meta.model()

    if request.method == 'GET':
        form = form(obj=obj)
    else:
        form = form(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template(template, form=form, key=None,
                           classes=("was-validated" if request.method == 'POST' else ''))

def generic_edit(form, template, id=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    
    obj = form.Meta.model.query.get(object_id)

    if request.method == 'GET':        
        form = form(obj=obj)
    else:
        form = form(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template(template, form=form, key=object_id,
                           classes=("was-validated" if request.method == 'POST' else ''))

def generic_delete(form, id):    
    obj = form.Meta.model.query.get(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")