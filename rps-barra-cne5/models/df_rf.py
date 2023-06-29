from flask import g
from pandas import DataFrame

from models.base import BaseModel
from models.base.model_enum import ModelEnum
from comp.BarraFactorYield.get_data_db import SourcesDataDB


class DfRf(BaseModel):
    """
    存贷款利率类型
    数据特性：自然日。取数范围：20070101至今

    """

    table_name = 'df_rf'
    columns = ['b_info_rate', 'b_info_benchmark', 'trade_dt']
    model_type = ModelEnum.MARKET_DATA
    start = "20070101"

    def create(self):
        g.ck.command("""
        create table if not exists df_rf
        (
            b_info_rate Nullable(Float64)
            ,b_info_benchmark Nullable(Float64)
            ,trade_dt FixedString(8)
        )
            engine = MergeTree ORDER BY trade_dt
                SETTINGS index_granularity = 8192
        """)

    def query_db(self, start, end) -> DataFrame:
        return SourcesDataDB().df_rf()

    def query_df(self, start, end) -> DataFrame:
        ck_sql = f"""select {','.join(self.columns)} from {self.table_name} where 
                          trade_dt between '{start}' and '{end}'
                         """
        return self.client.query_df(ck_sql)

    def delete(self, start, end):
        # 全清
        self.truncate()

    def insert_df(self, df: DataFrame):
        super().insert_df(df)

    def update(self, start, end):
        super().update(start, end)
