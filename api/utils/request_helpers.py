# coding: utf-8
from flask import request
from werkzeug.http import dump_cookie

# That's a workaround for explicitly setting SameSite to None
# Until the following fix is released:
# https://github.com/pallets/werkzeug/issues/1549
def set_cookie(response, *args, **kwargs):
    cookie = dump_cookie(*args, **kwargs)

    if 'samesite' in kwargs and kwargs['samesite'] is None:
        cookie = "{}; {}".format(cookie, b'SameSite=None')

    response.headers.add(
        'Set-Cookie',
        cookie
    )
