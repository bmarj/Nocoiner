# coding: utf-8
import datetime
import json
from flask import request

def get_filter_json():
    filter_json_req = json.loads(request.args.get('filter', '{"operands": []}'))
    filter_json = filter_json_req['operands']    
    days = request.args.get('days')
    if days and days != 'All':
        if days == 'All':
            days = 9999
        min_date = datetime.datetime.today() - datetime.timedelta(days=int(days))
        filter_json.append({'column':'purchase_date', 'condition':'>=', 'value':min_date})
    return filter_json


def get_sort_json():
    sort_json = json.loads(request.args.get('sortBy', '{ }'))
    return sort_json
    # sort_column = [{'field_name': k, 'direction': v} for k,v in sort_json.items()]
    # sorting = SortColumnSchema(many=True).load(sort_column, unknown=EXCLUDE)


def get_paging_json():
    paging_json = { 
        'page': int(request.args.get('page', '1')),
        'itemsPerPage': int(request.args.get('itemsPerPage', '10000'))
        }
    return paging_json
