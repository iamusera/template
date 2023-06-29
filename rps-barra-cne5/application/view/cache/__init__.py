from application.view.cache.view import cache_bp


def register_cache_views(app):
    """
    初始化蓝图
    """

    app.register_blueprint(cache_bp)
