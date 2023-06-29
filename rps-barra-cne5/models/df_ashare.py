from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfAshare(BaseModel):
    """

    数据特性：。取数范围：
    """

    table_name = 'df_ashare'
    columns = ['s_info_windcode', 'change_dt', 's_share_totala']
    model_type = ModelEnum.MARKET_DATA

    def create(self):
        g.ck.command("""
        create table if not exists df_ashare
        (
            s_info_windcode String
            ,change_dt FixedString(8)
            ,s_share_totala Nullable(Float64)
        )
            engine = MergeTree primary key (s_info_windcode)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_ashare()

    def query_df(self, start, end) -> DataFrame:
        return super().query_df(start, end)

    def delete(self, start, end):
        # 每次全量加载，全删
        super().truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
