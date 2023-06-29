from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfShibor(BaseModel):
    """

    数据特性：。取数范围：
    """

    table_name = 'df_shibor'
    columns = ['s_info_windcode', 'trade_dt', 'b_info_rate', 'b_info_term']
    model_type = ModelEnum.MARKET_DATA

    def create(self):
        g.ck.command("""
        create table if not exists df_shibor
        (
            s_info_windcode String
            ,trade_dt FixedString(8)
            ,b_info_rate Nullable(Float64)
            ,b_info_term Nullable(String)
        )
            engine = MergeTree order by (trade_dt)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_shibor()

    def query_df(self, start, end) -> DataFrame:
        return super().query_df(start, end)

    def delete(self, start, end):
        # 每次全量加载，全删
        super().truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
