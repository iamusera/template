from .exception_middleware import global_exception_handler
from .global_db import g_db, close_db


def init_middleware(app):
    global_exception_handler(app)
    app.before_request(g_db)
    app.teardown_appcontext(close_db)