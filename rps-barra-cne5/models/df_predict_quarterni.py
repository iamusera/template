from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfPredictQuarterni(BaseModel):
    """
    季报：分析师预测利润
    数据特性：每天算一遍近几年末报告期。取数范围：大于等于上一报告期
    """

    table_name = 'df_predict_quarterni'
    columns = ['s_info_compcode', 'est_report_dt', 'net_profit', 'ann_dt', 's_info_windcode']
    model_type = ModelEnum.FINA_REPORT

    def create(self):
        g.ck.command("""
        create table if not exists df_predict_quarterni
        (
            s_info_compcode String
            , est_report_dt FixedString(8)
            , net_profit Nullable(Float64)
            , ann_dt FixedString(8)
            , s_info_windcode String
        )
            engine = MergeTree ORDER BY est_report_dt
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().pd_predict_quarterni(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          est_report_dt between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                          est_report_dt between '{start}' and '{end}'
                         """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
