from flask import request, render_template, flash


def generic_add(formClass, template, id=None, submit_target=None):
    obj = formClass.Meta.model()

    if request.method == 'GET':
        form = formClass(obj=obj)
    else:
        form = formClass(request.values)

    if form.validate_on_submit():        
        form.populate_obj(obj)
        obj.query.session.add(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")
  
    return render_template(template, form=form, key=None, form_type=formClass.__name__, submit_target=submit_target,
                           classes=("was-validated" if request.method == 'POST' else ''))

def generic_edit(formClass, template, id=None, submit_target=None):
    """ Used for opening edit form and also POSTing values.
        Pattern used to reduce code duplication
    """
    object_id = id or request.values.get("key")
    
    obj = formClass.Meta.model.query.get(object_id)

    if request.method == 'GET':
        if request.values.get("action") == "copy":
            obj.id = None
            object_id = None
        form = formClass(obj=obj)
    else:
        form = formClass(request.values)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.query.session.commit()
        flash('Data saved', category="Success")
        return render_template("form_success.jinja")

    return render_template(template, form=form, key=object_id, form_type=formClass.__name__, submit_target=submit_target,
                           classes=("was-validated" if request.method == 'POST' else ''))

def generic_delete(form, id):    
    obj = form.Meta.model.query.get(id)
    obj.query.session.delete(obj)
    obj.query.session.commit()
    flash('Row deleted', category="Success")
    return render_template("form_success.jinja")


def generic_form_edit(submit_target, permitted_forms, id=None):
    """ Add/Edit object specified by form name
    """    
    object_id = id or request.values.get("key")
    object_type = request.values.get("form_type")
    form_class = [x for x in permitted_forms if x.__name__ == object_type][0]
    if not object_id:
        return generic_add(form_class, 'form_edit.jinja', None, submit_target)
    return generic_edit(form_class, 'form_edit.jinja', object_id, submit_target)

def generic_form_delete(permitted_forms, id):
    """ Delete object specified by form name
    """
    object_id = id or request.values.get("key")
    object_type = request.values.get("form_type")
    form_class = [x for x in permitted_forms if x.__name__ == object_type][0]
    return generic_delete(form_class, object_id)
