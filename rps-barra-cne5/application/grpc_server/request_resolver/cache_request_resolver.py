import simplejson

from application.grpc_server.request_resolver.base.base_request_resovler import BaseRequestResolver
from application.grpc_server.request_resolver.base.resolver_message import ResolverMessage
from application.view.cache import controller
from application.view.cache.validate import Param


class InitCache(BaseRequestResolver):
    def execute(self, json: str):
        param = Param(**simplejson.loads(json))
        result = controller.load_cache(param.tables, param.start, param.end)
        for e in iter(result):
            yield ResolverMessage.from_message(str(e))
