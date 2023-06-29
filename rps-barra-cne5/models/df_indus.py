from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfIndus(BaseModel):
    """
    申万行业
    数据特性：每天可能有变化。取数范围：申万行业，每次取全量
    """

    table_name = 'df_indus'
    columns = ['s_info_windcode', 'sw_ind_code', 'induscode',
               'entry_dt', 'remove_dt', 'cur_sign', 'industriesname']
    model_type = ModelEnum.BASE_INFO

    def create(self):
        g.ck.command("""
        create table if not exists df_indus
        (
            s_info_windcode String
            , sw_ind_code String
            , induscode String
            , entry_dt FixedString(8)
            , remove_dt Nullable(FixedString(8))
            , cur_sign FixedString(1)
            , industriesname String
        )
            engine = MergeTree ORDER BY (s_info_windcode, entry_dt)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_indus()

    def query_df(self, start, end) -> DataFrame:
        return super().query_df(start, end)

    def delete(self, start, end):
        # 每次全量加载，全删
        return super().truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
