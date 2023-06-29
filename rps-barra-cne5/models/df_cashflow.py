from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfCashflow(BaseModel):
    """
    现金流，数据特性：每天算一遍上一季度末报告期。取数范围：过去5年报告期滚动
    """

    table_name = 'df_cashflow'
    columns = ['s_info_windcode', 'report_period', 'ann_dt', 'actual_ann_dt',
               'statement_type', 'net_cash_flows_oper_act']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_cashflow
        (
            s_info_windcode String
            ,report_period FixedString(8)
            ,ann_dt Nullable(FixedString(8))
            ,actual_ann_dt Nullable(FixedString(8))
            ,statement_type String
            ,net_cash_flows_oper_act Nullable(Float64)
        )
            engine = MergeTree ORDER BY (report_period, ann_dt)
                SETTINGS index_granularity = 8192, allow_nullable_key = 1
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_cashflow(start, end)

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
