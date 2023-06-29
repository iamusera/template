from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfTradeDt(BaseModel):
    """
    交易日序列，全量拉取
    """

    table_name = 'df_trade_dt'
    columns = ['trade_dt']
    model_type = ModelEnum.MARKET_DATA

    def create(self):
        g.ck.command("""
        create table if not exists df_trade_dt
        (
            trade_dt String
        )
            engine = MergeTree primary key trade_dt ORDER BY trade_dt 
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_trade_dt()

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name}
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        self.truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
