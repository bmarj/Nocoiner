from __future__ import absolute_import
from operator import and_

from sqlalchemy.sql.sqltypes import String
from api.models.model_base import NonUnicodeString

import math
import json

from sqlalchemy import Text, func, or_
from sqlalchemy.dialects import mysql, postgresql, sqlite

from api.utils.model_helpers import get_column_in_models
from api.datatables.datatables_clean_regex import clean_regex
from api.datatables.datatables_search_methods import SEARCH_METHODS, search_operators


class DataTables:
    """Class defining a DataTables object.

    :param request: request containing the GET values, specified by the
        datatable for filtering, sorting and paging
    :type request: pyramid.request
    :param query: the query wanted to be seen in the the table
    :type query: sqlalchemy.orm.query.Query
    :param columns: columns specification for the datatables
    :type columns: list

    :returns: a DataTables object
    """

    def __init__(self, request, query, schema, related_model_classes=[], allow_regex_searches=False):
        """Initialize object and run the query."""
        self.params = dict(request)
        if 'sEcho' in self.params:
            raise ValueError(
                'Legacy datatables not supported, upgrade to >=1.10')
        self.query = query
        self.schema = schema
        self.related_model_classes = related_model_classes
        self.results = None
        self.allow_regex_searches = allow_regex_searches

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cardinality = 0

        self.yadcf_params = []
        self.filter_expressions = []
        self.error = None
        try:
            self.run()
        except Exception as exc:
            self.error = str(exc)

    def output_result(self):
        """Output results in the format needed by DataTables."""
        output = {}
        output['draw'] = int(self.params.get('draw', 1))
        output['recordsTotal'] = int(self.cardinality)
        output['recordsFiltered'] = int(self.cardinality_filtered)
        if self.error:
            output['error'] = self.error
            return output

        # output['data'] = self.schema.dump(self.results)
        output['data'] = self.results
        for k, v in self.yadcf_params:
            output[k] = v
        return output

    def _query_with_all_filters_except_one(self, query, exclude):
        return query.filter(*[
            e for i, e in enumerate(self.filter_expressions)
            if e is not None and i is not exclude
        ])

    # def _set_yadcf_data(self, query):
    #     # determine values for yadcf filters
    #     for i, col in enumerate(self.columns):
    #         if col.search_method in 'yadcf_range_number_slider':
    #             v = query.add_columns(
    #                 func.min(col.sqla_expr), func.max(col.sqla_expr)).one()
    #             self.yadcf_params.append(('yadcf_data_{:d}'.format(i),
    #                                       (math.floor(v[0]), math.ceil(v[1]))))
    #         if col.search_method in [
    #                 'yadcf_select', 'yadcf_multi_select', 'yadcf_autocomplete'
    #         ]:
    #             filtered = self._query_with_all_filters_except_one(
    #                 query=query, exclude=i)
    #             v = filtered.add_columns(col.sqla_expr).distinct().all()
    #             self.yadcf_params.append(('yadcf_data_{:d}'.format(i),
    #                                       [r[0] for r in v]))

    def run(self):
        """Launch filtering, sorting and paging to output results."""
        query = self.query

        # apply data domain context
        self._set_context_filter_expression()
        query = query.filter(
            *[e for e in self.filter_expressions if e is not None])
        # count before filtering
        self.cardinality = query.count()
        
        self._set_column_filter_expressions()
        self._set_global_filter_expression()
        self._set_sort_expressions()
        # self._set_yadcf_data(query)

        # apply filters
        query = query.filter(
            *[e for e in self.filter_expressions if e is not None])

        self.cardinality_filtered = query.count()

        # apply sorts
        query = query.order_by(
            *[e for e in self.sort_expressions if e is not None])

        # add paging options
        length = int(self.params.get('length'))
        if length >= 0:
            query = query.limit(length)
        elif length == -1:
            pass
        else:
            raise (ValueError(
                'Length should be a positive integer or -1 to disable'))
        query = query.offset(int(self.params.get('start')))

        self.results = self.schema.dump(query.all())

        # # add columns to query
        # query = query.add_columns(*[c.sqla_expr for c in self.columns])

        # # fetch the result of the queries
        # column_names = [
        #     col.mData if col.mData else str(i)
        #     for i, col in enumerate(self.columns)
        # ]
        # self.results = [{k: v
        #                  for k, v in zip(column_names, row)}
        #                 for row in query.all()]

    def _set_context_filter_expression(self):
        # filtering contextual or detail grids
        i = 0
        while self.params.get('filtered_by[{:d}][field]'.format(i), False):
            column_name = self.params.get('filtered_by[{:d}][field]'.format(i), False)
            value = self.params.get('filtered_by[{:d}][value]'.format(i), None)
            i += 1

            models = self.query.get_model_classes()
            column = get_column_in_models(models, column_name)

            if column and value is not None:
                filter_expr = column == value
                self.filter_expressions.append(filter_expr)


    def _set_column_filter_expressions(self):
        """Construct the query: filtering.

        Add filtering when per column searching is used.
        """
        columns = []
        models = self.query.get_model_classes()
        i = 0
        while self.params.get('columns[{:d}][data]'.format(i), False):
            column_name = self.params.get('columns[{:d}][data]'.format(i))
            value = self.params.get('columns[{:d}][search][value]'.format(i),
                                    '')
            searchable = self.params.get('columns[{:d}][searchable]'.format(i),
                                         'false')
            is_regex = self.params.get('columns[{:d}][search][regex]'.format(i),
                                    '') == 'true'
            i += 1
            if searchable.lower() == 'false':
                continue
            search_val = value
            if is_regex:
                if search_val.startswith('^'):
                    search_val = search_val.replace('^','') + '%'
            else:
                if search_val != '':
                    search_val = '%' + search_val + '%'

            column = get_column_in_models(models, column_name)
            if column:
                columns.append([column, search_val])

        # per columns filters:
        for column, value in columns:
            filter_expr = None
            if value:
                search_func = SEARCH_METHODS['like']
                filter_expr = search_func(column, value)
            self.filter_expressions.append(filter_expr)

    def _set_global_filter_expression(self):
        # global search filter
        global_search = self.params.get('search[value]', '')
        if global_search == '':
            return

        columns = []
        models = self.query.get_model_classes()
        i = 0
        while self.params.get('columns[{:d}][data]'.format(i), False):
            column_name = self.params.get('columns[{:d}][data]'.format(i))
            searchable = self.params.get('columns[{:d}][searchable]'.format(i),
                                         'false')
            i += 1
            if searchable.lower() == 'false':
                continue
            column = get_column_in_models(models, column_name)
            if column:
                columns.append(column)

        if (self.allow_regex_searches
                and self.params.get('search[regex]') == 'true'):
            op = self._get_regex_operator()
            val = clean_regex(global_search)

            def filter_for(col):
                return col.op(op)(val)
        else:
            # TODO: refine, extract and make configurable/pluggable,
            #       at least for most important use cases

            def filter_for(col):
                """ Filtering for datatable Search field.
                    Applies some application specific column filtering rules.
                    example: 'begi' search non-numeric columns for content that begins with searched prefix
                             'word ' (with space afterwards) search whole word on textual columns
                             '>=1' search numeric columns grater than 1

                """
                val = '' + global_search + ''
                search_func = SEARCH_METHODS['like']
                val_without_ops = val
                if global_search.startswith(tuple(search_operators.keys())):
                    has_expr = True
                    val_without_ops = val_without_ops.lstrip('<').lstrip('>').lstrip('=')
                else:
                    has_expr = False
                
                if col.type.__visit_name__ == 'unicode':
                    if has_expr:
                        return None
                    try:
                        if global_search.endswith(' '):
                            return or_(search_func(col, global_search.strip()),
                                       search_func(col, global_search + '%') )
                        else:
                            val = global_search + '%'
                            search_func = SEARCH_METHODS['like']
                    except:
                        return None
                elif col.type.__class__ is String or col.type.__class__ is NonUnicodeString:
                    if has_expr:
                        return None                    
                    try:
                        if global_search.endswith(' '):
                            return or_(search_func(col, global_search.strip()),
                                       search_func(col, global_search + '%') )
                        else:
                            val = global_search + '%'
                            search_func = SEARCH_METHODS['like']
                    except:
                        return None
                elif col.type.__visit_name__ == 'integer' and has_expr:
                    if not val_without_ops.isdigit():
                        return None
                    search_func = SEARCH_METHODS['like']
                    val = global_search.strip()
                elif col.type.__visit_name__ == 'NUMERIC' and has_expr:
                    if not val_without_ops.lstrip('-').replace(',','').replace('.','').strip().isdigit():
                        return None
                    search_func = SEARCH_METHODS['numeric']
                    val = global_search.strip()
                # elif col.type.__visit_name__ == 'datetime':
                #     return None
                #     # search_func = SEARCH_METHODS['date']
                else:
                    if has_expr:
                        return None
                    # WARNING: this search remaining column types by converting them to string!
                    #          For performance reasons, this needs to be removed for larger data.
                    return col.cast(Text).like('%' + val + '%')
                if not search_func:
                    return None
                try:
                    filter_expr = search_func(col, val)
                except:
                    return None
                return filter_expr

        global_filter = [
            filter_for(col) for col in columns if filter_for(col) is not None # if hasattr(col, 'global_search') and col.global_search
        ]

        self.filter_expressions.append(or_(*global_filter))

    def _set_sort_expressions(self):
        """Construct the query: sorting.

        Add sorting(ORDER BY) on the columns needed to be applied on.
        """
        sort_expressions = []
        models = self.query.get_model_classes()
        i = 0
        while self.params.get('order[{:d}][column]'.format(i), False):
            column_nr = int(self.params.get('order[{:d}][column]'.format(i)))
            column_name = self.params.get('columns[{:d}][data]'.format(column_nr))
            direction = self.params.get('order[{:d}][dir]'.format(i))
            orderable = self.params.get('columns[{:d}][orderable]'.format(column_nr),
                                        'false')
            i += 1

            if orderable.lower() == 'false':
                continue

            # for sorting on related columns, query must use JOIN with related table
            column = get_column_in_models(models, column_name)

            if not column:
                # # making sorting by unknown column not fatal
                continue
                # raise Exception('Invalid sort column: %s' % column_name)

            sort_expr = column
            if direction == 'asc':
                sort_expr = sort_expr.asc()
            elif direction == 'desc':
                sort_expr = sort_expr.desc()
            else:
                raise ValueError(
                    'Invalid order direction: {}'.format(direction))
            # if column.nulls_order:
            #     if column.nulls_order == 'nullsfirst':
            #         sort_expr = sort_expr.nullsfirst()
            #     elif column.nulls_order == 'nullslast':
            #         sort_expr = sort_expr.nullslast()
            #     else:
            #         raise ValueError(
            #             'Invalid order direction: {}'.format(direction))
            sort_expressions.append(sort_expr)

        self.sort_expressions = sort_expressions

    def _get_regex_operator(self):
        if isinstance(self.query.session.bind.dialect, postgresql.dialect):
            return '~'
        elif isinstance(self.query.session.bind.dialect, mysql.dialect):
            return 'REGEXP'
        elif isinstance(self.query.session.bind.dialect, sqlite.dialect):
            return 'REGEXP'
        else:
            raise NotImplementedError(
                'Regex searches are not implemented for this dialect')
