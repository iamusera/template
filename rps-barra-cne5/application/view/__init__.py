from application.view.index import register_index_views
from application.view.cache import register_cache_views


def init_view(app):
    register_index_views(app)
    register_cache_views(app)
