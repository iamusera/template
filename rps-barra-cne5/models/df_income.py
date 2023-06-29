from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfIncome(BaseModel):
    """
    季报总营业收入
    数据特性：每天算一遍上一季度末报告期。取数范围：过去5年滚动
    """

    table_name = 'df_income'
    columns = ['tot_oper_rev', 'net_profit_excl_min_int_inc', 'net_profit_incl_min_int_inc', 's_fa_eps_basic',
               's_fa_eps_diluted', 's_info_windcode', 'report_period', 'ann_dt', 'actual_ann_dt', 'statement_type']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_income
        (
            tot_oper_rev Nullable(Float64)
            , net_profit_excl_min_int_inc Nullable(Float64)
            , net_profit_incl_min_int_inc Nullable(Float64)
            , s_fa_eps_basic Nullable(Float64)
            , s_fa_eps_diluted Nullable(Float64)
            , s_info_windcode String
            , report_period FixedString(8)
            , ann_dt Nullable(FixedString(8))
            , actual_ann_dt Nullable(FixedString(8))
            , statement_type String
        )
            engine = MergeTree ORDER BY (report_period, ann_dt)
                SETTINGS index_granularity = 8192, allow_nullable_key = 1
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_income(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          ann_dt between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                          ann_dt between '{start}' and '{end}'
                         """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
