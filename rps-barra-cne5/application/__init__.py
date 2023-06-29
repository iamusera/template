import os
from flask import Flask
from application.configs import get_cfg
from application.extensions import init_plugs
from application.middleware import global_exception_handler, init_middleware
from application.view import init_view
from celery_app.celery_process import init_celery, celery_app
from models import add_tables


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # 从本地环境中读取
    config_name = os.getenv('FLASK_CONFIG', 'dev')
    print(f' * env_config: {config_name}')

    # 配置
    app.config.update(get_cfg(config_name))

    # 注册工具
    init_plugs(app)

    # 注册中间件
    init_middleware(app)

    # 注册路由
    init_view(app)

    # 注册celery
    init_celery(app, celery_app)

    # 注册缓存ck
    add_tables()

    return app


# app = create_app()
