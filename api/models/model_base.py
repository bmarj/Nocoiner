# coding: utf-8
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.dialects import postgresql
from sqlalchemy import desc, types, NUMERIC
from sqlalchemy.dialects.mssql import (BIT, DECIMAL,
                                       DATETIMEOFFSET)
from api.utils.model_helpers import get_column_in_models

DEFAULT_COLLATION = "ascii"

class Numeric(NUMERIC):
    """
    Fix Decimal type for serialization problem,
    with asdecimal=False as default
    If using original class, use type Numeric(10, 2, asdecimal=False)
    """
    def __init__(self, precision=None, scale=None, decimal_return_scale=None, asdecimal=False):
        super().__init__(precision, scale, decimal_return_scale, asdecimal)


class NonUnicodeString(types.TypeDecorator):
    """
    Type for VARCHAR columns,
    renders value in sql query predicate without N Unicode prefix.
    """
    impl = types.String

    def process_bind_param(self, value, dialect):
        # TODO: setup other encodings, 
        if isinstance(dialect, postgresql.dialect):
            return value
        return bytes(value, self.impl.collation or DEFAULT_COLLATION)

# doesn't work:
# https://github.com/sqlalchemy/sqlalchemy/issues/4442#issuecomment-453875342
# class NonUnicodeStringDecorator(TypeDecorator):
#     impl = types.String
#     def literal_processor(self, dialect):
#         def process(value):
#             value = value.replace("'", "''")
#             if dialect.identifier_preparer._double_percents:
#                 value = value.replace("%", "%%")
#             return "'%s'" % value
#         return process


class CustomSQLAlchemy(SQLAlchemy):
    MONEY = Numeric(18, 2)
    BIT = BIT
    DATETIMEOFFSET = DATETIMEOFFSET


class CustomQuery(BaseQuery):
    def get_model_classes(self, related_model_classes=[]):
        q_state = self._compile_state()
        main_model_class = q_state._entity_zero().entity  # returns the query's Model
        model_classes = [main_model_class] + related_model_classes + \
                        [ent.entity for ent in q_state._join_entities]
        return model_classes

db = CustomSQLAlchemy(query_class=CustomQuery)


# adapted from: https://ruddra.com/dynamically-constructing-filters-based-on-string-input-using-sqlalchemy/
def filter_query(query, filter_condition, related_model_classes=[]):
    '''
    Return filtered queryset based on condition.
    :param query: takes query
    :param filter_condition: Its a list, ie: [(key,operator,value)]
    operator list:
        eq for ==
        lt for <
        ge for >=
        in for in_
        like for like
        value could be list or a string
    :return: queryset
    '''
    if query is None:
        return query  # query = self.get_query()
    q_state = query._compile_state()
    main_model_class = q_state._entity_zero().entity  # returns the query's Model
    model_classes = [main_model_class] + related_model_classes + \
                    [ent.entity for ent in q_state._join_entities]
    for raw in filter_condition:
        try:
            key = raw['column']
            op = raw['condition']\
                .replace('!=', 'ne')\
                .replace('<>', 'ne')\
                .replace('>=', 'ge')\
                .replace('<=', 'le')\
                .replace('==', 'eq')\
                .replace('=', 'eq')\
                .replace('<', 'lt').replace('>', 'gt')\
                .replace('like', 'contains')
            value = raw['value']
        except ValueError:
            raise Exception('Invalid filter: %s' % raw)
        column = get_column_in_models(model_classes, key, None)
        if not column:
            raise Exception('Invalid filter column: %s' % key)
        if op == 'in':
            if isinstance(value, list):
                filt = column.in_(value)
            else:
                filt = column.in_(value.split(','))
        else:
            try:
                attr = list(filter(
                    lambda e: hasattr(column, e % op),
                    ['%s', '%s_', '__%s__']
                ))[0] % op
            except IndexError:
                raise Exception('Invalid filter operator: %s' % op)
            if value == 'null' or value == '':
                value = None
            filt = getattr(column, attr)(value)
        query = query.filter(filt)
    return query

def sort_query(query, sort_json, related_model_classes=[]):
    q_state = query._compile_state()
    main_model_class = q_state._entity_zero().entity  # returns the query's Model
    model_classes = [main_model_class] + related_model_classes + \
                    [ent.entity for ent in q_state._join_entities]
    for (key, v) in sort_json.items():
        column = get_column_in_models(model_classes, key, None)
        if not column:
            # making sorting by unknown column not fatal
            continue
            # raise Exception('Invalid sort column: %s' % key)
        if v == -1:
            query = query.order_by(desc(column))
        else:
            query = query.order_by(column)
    return query

def paginate_query(query, pagination):
    return query.paginate(pagination['page'], pagination['itemsPerPage'])

def get_model_changes(model, fk_column_name):
    """
    from: https://stackoverflow.com/questions/29921260/tracking-model-changes-in-sqlalchemy

    Return a dictionary containing changes made to the model since it was
    fetched from the database.

    The dictionary is of the form {'property_name': [old_value, new_value]}

    Example:
        user = get_user_by_id(420)
        >>> '<User id=402 email="business_email@gmail.com">'
        get_model_changes(user)
        >>> {}
        user.email = 'new_email@who-dis.biz'
        get_model_changes(user)
        >>> {'email': ['business_email@gmail.com', 'new_email@who-dis.biz']}
    """
    state = db.inspect(model)
    changes = []
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)

        if not hist.has_changes():
            continue

        old_value = hist.deleted[0] if hist.deleted else None
        new_value = hist.added[0] if hist.added else None
        changes.append({
            fk_column_name: state.identity[0],
            "column_name": attr.key,
            "old_value": old_value,
            "new_value": new_value
        })

    return changes

def has_model_changed(model):
    """
    Return True if there are any unsaved changes on the model.
    """
    return bool(get_model_changes(model, "id"))
