from abc import ABC

from clickhouse_connect.driver import Client
from flask import g
from pandas import DataFrame

from models.base.model_enum import ModelEnum
from application.extensions.init_clickhouse import ck_client

class BaseModel(ABC):
    table_name = None
    columns = []
    start = None

    @property
    def client(self) -> Client:
        ck: Client = ck_client()
        try:
            ck.ping()
        finally:
            pass
        return ck

    @property
    def model_type(self) -> ModelEnum:
        """
            模型类型
            运行时会取到子类的model_type
        :return:
        """
        return self.model_type

    def drop(self):
        self.client.command(f"drop table if exists {self.table_name}")

    def create(self):
        ...

    def truncate(self):
        self.client.command(f"truncate table {self.table_name}")

    def query_db(self, start, end) -> DataFrame:
        ...

    def query_df(self, start, end) -> DataFrame:
        return self.client.query_df(f"select {','.join(self.columns)} from {self.table_name}")

    def delete(self, start, end):
        ...

    def insert_df(self, df: DataFrame):

        len1 = len(df)
        GROUP_SIZE = 1_000_000
        if len1 > GROUP_SIZE:
            # 将数据框按照行数拆分成多个，根据网络环境的情况确定拆分粒度
            for i in range(0, len1, GROUP_SIZE):
                subDf = df[i: i + GROUP_SIZE - 1]
                # 将每个分组保存
                self.client.insert(self.table_name, subDf, list(subDf.columns))
        else:
            # 批量插入，这里需要指定columns，避免顺序不一致的问题
            self.client.insert(self.table_name, df, list(df.columns))

    def update(self, start, end):
        ...
