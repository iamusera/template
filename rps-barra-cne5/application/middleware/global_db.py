from flask import g
from application.extensions.init_clickhouse import ck_client


def g_db():
    g.ck = ck_client()


def close_db(error):
    if hasattr(g, 'ck'):
        g.ck.close()
