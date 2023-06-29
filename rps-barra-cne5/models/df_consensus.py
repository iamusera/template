from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfConsensus(BaseModel):
    """

    数据特性：。取数范围：
    """

    table_name = 'df_consensus'
    columns = ['s_info_windcode', 'est_dt', 'est_report_dt', 'eps_avg',
               'net_profit_avg', 's_est_yeartype', 'consen_data_cycle_typ']
    # 与财报的逻辑类似
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_consensus
        (
            s_info_windcode String
            ,est_dt FixedString(8)
            ,est_report_dt FixedString(8)
            ,eps_avg Nullable(Float64)
            ,net_profit_avg Nullable(Float64)
            ,s_est_yeartype Nullable(String)
            ,consen_data_cycle_typ Nullable(String)
        )
            engine = MergeTree order by (est_dt,est_report_dt)
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_consensus(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          est_dt between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                                  est_dt between '{start}' and '{end}'
                                 """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
