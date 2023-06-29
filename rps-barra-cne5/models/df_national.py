from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfNational(BaseModel):
    """

    数据特性：。取数范围：
    """

    table_name = 'df_national'
    columns = ['s_info_windcode', 's_info_compcode', 's_info_compname', 's_info_countryname', 'crncy_name',
               'security_status']
    model_type = ModelEnum.BASE_INFO

    def create(self):
        g.ck.command("""
        create table if not exists df_national
        (
            s_info_windcode String
            ,s_info_compcode String
            ,s_info_compname Nullable(String)
            ,s_info_countryname Nullable(String)
            ,crncy_name Nullable(String)
            ,security_status UInt64
        )
            engine = MergeTree primary key (s_info_windcode)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_national()

    def query_df(self, start, end) -> DataFrame:
        return super().query_df(start, end)

    def delete(self, start, end):
        # 每次全量加载，全删
        super().truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
