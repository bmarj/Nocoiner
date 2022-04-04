# coding: utf-8

def get_column_in_models(model_classes, key, default=None):
    column, model_class = find_column_in_models(model_classes, key, default)
    return column

def find_column_in_models(model_classes, property_path, default=None):
    # if it is related column, use column name
    key = property_path.split('.')[-1]
    model_list = model_classes
    if not hasattr(model_classes, '__iter__'):
        model_list = [model_classes]
    for model_class in model_list:
        column = getattr(model_class, key, None)
        if column:
            return column, model_class
    return default, None

def find_column_in_models_deep(model_classes, property_path, default=None):
    paths = property_path.split('.')
    model_list = model_classes
    if not hasattr(model_classes, '__iter__'):
        model_list = [model_classes]
    for model_class in model_list:
        column = getattr(model_class, paths[0], None)
        if column and hasattr(column.property, 'entity'):
            return find_column_in_models(column.property.entity.entity,
                                         '.'.join(paths[1:]),
                                         default)
        # else:
        #     return column, model_class
        # found, last one in path
        if column and len(paths) == 1:
            return column, model_class
    return default, None
