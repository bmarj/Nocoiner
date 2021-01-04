from dataclasses import dataclass
#from typing import Optional, List
from marshmallow import Schema, fields, validate, pre_load

@dataclass
class Sorting:
    field_name: str
    direction: int


@dataclass
class Paging:
    page: int
    items_per_page: int


class SortColumnSchema(Schema):
    field_name = fields.Str(required=True)
    direction = fields.Int()
    purchase_date = fields.Int()

    # @pre_load
    # def unpivot(self, data, many, **kwargs):
    #     for k, v in data.items():
    #         self.fields['field_name'] = k
    #         self.fields['direction'] = v


# class SortingSchema(Schema):
#     # columns = fields.Dict(keys=fields.String(), values=fields.Nested(SortColumnSchema))
# #     sortBy = fields.Dict(keys=fields.String(), values=fields.Dict())
#     sortBy = fields.Nested(SortColumnSchema)
#     field_name = fields.Str(required=False)
#     direction = fields.Int()

#     # @pre_load
#     # def unpivot(self, data, many, **kwargs):
#     #     return ""

#     # @post_load
#     # def trans_friends(self, item):
#     #     pass
#         # for name in item['columns']:
#         #     item['columns'][name] = ['friends'] = [item['columns'][n] for n in item['columns'][name]['friends']]


class PagingSchema(Schema):
    page = fields.Int(required=True)
    items_per_page = fields.Int(required=True)