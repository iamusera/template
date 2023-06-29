from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB

class DfWindqa(BaseModel):
    """
    Wind全A指数收盘价
    数据特性：交易日有数据。取数范围：过去252交易日滚动
    """

    table_name = 'df_windqa'
    columns = ['s_info_windcode', 'trade_dt', 's_dq_close']
    model_type = ModelEnum.MARKET_DATA

    def create(self):
        g.ck.command("""
        create table if not exists df_windqa
        (
            s_info_windcode String,
            trade_dt        FixedString(8),
            s_dq_close Nullable(Float64)
        )
            engine = MergeTree ORDER BY trade_dt
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_windqa(start, end)

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          trade_dt between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        ck_sql = f"""alter table {self.table_name} delete where 
                          trade_dt between '{start}' and '{end}'
                         """
        return self.client.command(ck_sql)

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
