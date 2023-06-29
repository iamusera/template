from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfFyyoy(BaseModel):
    """
    年报：一致预期净利润FY0，FY3，YOY，
    数据特性：每天算一遍近几年末报告期。取数范围：大于等于上一报告期
    """

    table_name = 'df_fyyoy'
    columns = ['net_profit', 's_info_windcode', 'est_dt', 'rolling_type', 'benchmark_yr']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_fyyoy
        (
            net_profit Nullable(Float64)
            , s_info_windcode String
            , est_dt FixedString(8)
            , rolling_type String
            , benchmark_yr FixedString(8)
        )
            engine = MergeTree ORDER BY benchmark_yr
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_fyyoy(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          benchmark_yr between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                          benchmark_yr between '{start}' and '{end}'
                         """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
