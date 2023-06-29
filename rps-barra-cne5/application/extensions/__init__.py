from flask import Flask

from .init_grpc import init_grpc
from .init_sqlalchemy import init_databases
from .loguru import init_log


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_log(app)
    # init_loguru(app)
    init_grpc(app)
