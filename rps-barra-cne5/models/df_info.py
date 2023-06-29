from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfInfo(BaseModel):
    """
    股票信息
    数据特性：取全量。取数范围：每次取全量
    """

    table_name = 'df_info'
    columns = ['s_info_windcode', 's_info_listdate', 's_info_exchmarket', 's_info_delistdate', 'bs_info_delistdate']
    model_type = ModelEnum.BASE_INFO

    def create(self):
        g.ck.command("""
        create table if not exists df_info
        (
            s_info_windcode String
            ,s_info_listdate Nullable(FixedString(8))
            ,s_info_exchmarket String
            ,s_info_delistdate Nullable(String)
            ,bs_info_delistdate Nullable(String)
        )
            engine = MergeTree primary key (s_info_windcode)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_info()

    def query_df(self, start, end) -> DataFrame:
        return super().query_df(start, end)

    def delete(self, start, end):
        # 每次全量加载，全删
        super().truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
