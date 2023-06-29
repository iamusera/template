from flask import Blueprint, request
from application.responses import SuccessResponse
from application.view.cache import controller
# from application.view.cache.controller import _load_cache
from application.view.cache.validate import Param, ShardParam

cache_bp = Blueprint('cache', __name__, url_prefix='/')


@cache_bp.get('/cache/init_table')
def init_table():
    controller.init_table()
    return SuccessResponse().result()


@cache_bp.get('/cache/recreate_table')
def recreate_table():
    tables = request.args.get('tables', type=str)
    if tables:
        table_list = [x.strip() for x in tables.split(',')]
    else:
        table_list = []
    controller.recreate_table(table_list)
    return SuccessResponse().result()


@cache_bp.get('/cache/init_cache')
def init_cache():
    tables = request.args.get('tables', type=str)
    if tables:
        table_list = [x.strip() for x in tables.split(',')]
    else:
        table_list = []
    return SuccessResponse(data=controller.init_cache(table_list)).result()


@cache_bp.get('/cache/init_cache_shard')
def init_cache_shard():
    curr = request.args.get('curr', type=int)
    total = request.args.get('total', type=int)
    param = ShardParam(curr, total)
    return SuccessResponse(controller.init_cache_shard(param.curr, param.total)).result()


@cache_bp.post('/cache/increase_cache')
def increase_cache():
    json = request.get_json()
    param = Param(**json)
    return SuccessResponse(controller.increase_cache(param.tables, param.start, param.end)).result()


@cache_bp.post('/cache/query_cache')
def query_cache():
    json = request.get_json()
    param = Param(**json)
    controller.query_cache(param.tables, param.start, param.end)
    return SuccessResponse().result()
