from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# use will initilaize it by using:
# from utils.rate_limiter import limiter
# limiter.init_app(app)

# def init_app(app):
#     global limiter
#     limiter = Limiter(app, key_func=lambda: "all")
