from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfTtm(BaseModel):
    """
    季报 净利润TTM 现金收益TTM
    数据特性：季度末报告期。取数范围：过去5年滚动
    """

    table_name = 'df_ttm'
    columns = ['s_fa_profit_ttm', 's_fa_operatecashflow_ttm', 's_info_windcode', 'report_period', 'statement_type']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_ttm
        (
            s_fa_profit_ttm Nullable(Float64)
            ,s_fa_operatecashflow_ttm Nullable(Float64)
            ,s_info_windcode String
            ,report_period FixedString(8)
            ,statement_type FixedString(10)
        )
            engine = MergeTree ORDER BY report_period
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_ttm(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          report_period between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                          report_period between '{start}' and '{end}'
                         """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
