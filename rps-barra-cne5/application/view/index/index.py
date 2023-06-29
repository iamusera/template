import time

import numpy as np
import pandas as pd
from clickhouse_connect.driver import Client
from flask import Blueprint, jsonify, g
from loguru import logger
import datetime

from application.responses import SuccessResponse, FailureResponse
from comp.BarraFactorYield.DataProcess import DataProcess
from application.common.utils.db_dao import DB

from pandas.api.types import is_datetime64_any_dtype

index_bp = Blueprint('Index', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    DataProcess().run()
    return SuccessResponse(data=[]).result()


@index_bp.route('/test')
def test():
    logger.info("hello world！")
    return SuccessResponse(data=[]).result()


@index_bp.route('/test/wind_db')
def test_wind_db():
    logger.info("query default db wind db！")
    data = DB.execute_sql("select 1 from dual")
    logger.info("query result: {}", data)
    return SuccessResponse(data=[]).result()


@index_bp.route('/test/rps_db')
def test_rps_db():
    logger.info("query default db wind db！")
    data = DB.execute_sql("select 1 from dual", "rps_db")
    logger.info("query result: {}", data)
    return SuccessResponse(data=[]).result()


@index_bp.route('/test/ck_db')
def test_ck_db():
    logger.info("query default db wind db！")
    client: Client = g.ck
    data = client.query_df("select 1 as res")
    logger.info("query result: \n{}", data)
    return SuccessResponse(data=[]).result()
