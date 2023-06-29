#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
    @Author：iamusera
    @date：2023-02-17 12:01
    @description: 
"""
from .base import MetaData, BaseModel
from .df_cashflow import DfCashflow
from .df_fyyoy import DfFyyoy
from .df_income import DfIncome
from .df_indus import DfIndus
from .df_info import DfInfo
from .df_predict_quarterni import DfPredictQuarterni
from .df_rf import DfRf
from .df_trade_dt import DfTradeDt
from .df_ttm import DfTtm
from .df_windqa import DfWindqa
from .df_otherindex import DfOtherindex
from .df_volume_share import DfVolumeShare
from .df_stockprice_tradingvolume import DfStockpriceTradingvolume
from .df_assetbalance import DfAssetbalance
from .df_national import DfNational
from .df_shibor import DfShibor
from .df_ashare import DfAshare
from .df_consensus import DfConsensus


def add_tables():
    meta = MetaData()
    table_dict = {
        DfWindqa.table_name: DfWindqa,
        DfOtherindex.table_name: DfOtherindex,
        DfVolumeShare.table_name: DfVolumeShare,
        DfStockpriceTradingvolume.table_name: DfStockpriceTradingvolume,
        DfAssetbalance.table_name: DfAssetbalance,
        DfInfo.table_name: DfInfo,
        DfIncome.table_name: DfIncome,
        DfPredictQuarterni.table_name: DfPredictQuarterni,
        DfFyyoy.table_name: DfFyyoy,
        DfRf.table_name: DfRf,
        DfTtm.table_name: DfTtm,
        DfTradeDt.table_name: DfTradeDt,
        DfCashflow.table_name: DfCashflow,
        DfIndus.table_name: DfIndus,
        DfNational.table_name: DfNational,
        DfShibor.table_name: DfShibor,
        DfAshare.table_name: DfAshare,
        DfConsensus.table_name: DfConsensus
    }

    # 通过meta.tables 获取表对象, 跑批等处理
    meta.add_dict(table_dict)

    # 执行所有的ddl初始化schema
    # for model_clas in meta.tables.values():
    #     model_obj: BaseModel = model_clas()
    #     model_obj.create()


def get_tables():
    meta = MetaData()
    return meta.tables
