#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2022-12-06 17:32
"""

from application.extensions.init_sqlalchemy import db
from sqlalchemy import MetaData, Table, text

import pandas as pd


class DB:
    """
    数据库类
    """

    @classmethod
    def execute_sql(cls, sql, engine_=None):
        """ 执行原生sql """
        engine = db.get_engine(engine_)
        with engine.connect() as connection:
            with connection.begin() as trans:
                # The Transaction object is not threadsafe.
                data = connection.execute(text(sql))
                if data.returns_rows:
                    data = data.fetchall()
                    # data = list(map(lambda x: dict(x.items()), data))
                    # data = list(map(lambda x: tuple(x), data))
                trans.commit()
        return data

    @classmethod
    def map_table(cls, table_name, con):
        """ 获取数据库的映射 """
        metadata_obj = MetaData()
        # reflect individual table
        t = Table(table_name, metadata_obj, autoload_with=con)
        return t

    @classmethod
    def orm_insert(cls, table_name, value, engine_=None):
        """ 映射数据库之后， 批量的插入/单条插入 """
        engine = db.get_engine(engine_)
        with engine.begin() as con:
            table = cls.map_table(table_name, con)
            con.execute(table.insert(), value)
            con.commit()

    @classmethod
    def pd_read_sql(cls, sql, engine_=None):
        """ pandas read sql """
        engine = db.get_engine(engine_)
        with engine.begin() as con:
            return pd.read_sql(text(sql), con)

    @classmethod
    def execute_many(cls, sql, data, engine_=None):
        # mysql&clickhouse&pg, oracle不支持
        # 批量插入，没有测试np.nan是否支持
        engine = db.get_engine(engine_)
        with engine.connect() as connection:
            with connection.begin() as trans:
                connection.connection.cursor().executemany(sql, data)
                trans.commit()
