from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfAssetbalance(BaseModel):
    """
    资产负债表，数据特性：每天算一遍上一季度末报告期。取数范围：过去5年报告期滚动
    """

    table_name = 'df_assetbalance'
    columns = ['s_info_windcode', 'report_period', 'ann_dt', 'actual_ann_dt', 'statement_type',
               'tot_shrhldr_eqy_incl_min_int', 'tot_shrhldr_eqy_excl_min_int',
               'other_equity_tools_p_shr', 'other_sustainable_bond', 'tot_assets', 'tot_liab', 'tot_non_cur_liab',
               'tot_cur_liab', 'lt_borrow', 'bonds_payable', 'lease_liab']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_assetbalance
        (
            s_info_windcode Nullable(String)
            ,report_period  FixedString(8)
            ,ann_dt         Nullable(String)
            ,actual_ann_dt  Nullable(String)
            ,statement_type Nullable(String)
            ,tot_shrhldr_eqy_incl_min_int Nullable(Float64)
            ,tot_shrhldr_eqy_excl_min_int Nullable(Float64)
            ,other_equity_tools_p_shr Nullable(Float64)
            ,other_sustainable_bond Nullable(Float64)
            ,tot_assets Nullable(Float64)
            ,tot_liab Nullable(Float64)
            ,tot_non_cur_liab Nullable(Float64)
            ,tot_cur_liab Nullable(Float64)
            ,lt_borrow Nullable(Float64)
            ,bonds_payable Nullable(Float64)
            ,lease_liab Nullable(Float64)
        )
            engine = MergeTree ORDER BY (report_period, ann_dt)
                SETTINGS index_granularity = 8192, allow_nullable_key = 1
        """)
        # ann_dt actual_ann_dt 出现空值 report_period=20070630

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_assetbalance(start, end)

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
