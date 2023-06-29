from models import *
from .get_data_db import SourcesDataDB

IS_USE_CACHE = True


class SourcesDataCache(SourcesDataDB):

    def df_windqa(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfWindqa().query_df(daily_start, daily_end)
        return super().df_windqa(daily_start, daily_end)

    def df_otherindex(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfOtherindex().query_df(daily_start, daily_end)
        return super().df_otherindex(daily_start, daily_end)

    def df_volume_share(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfVolumeShare().query_df(daily_start, daily_end)
        return super().df_volume_share(daily_start, daily_end)

    def df_stockprice_tradingvolume(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfStockpriceTradingvolume().query_df(daily_start, daily_end)
        return super().df_stockprice_tradingvolume(daily_start, daily_end)

    def df_assetbalance(self, quarter_start, quarter_end):
        if IS_USE_CACHE:
            return DfAssetbalance().query_df(quarter_start, quarter_end)
        return super().df_assetbalance(quarter_start, quarter_end)

    def df_info(self):
        if IS_USE_CACHE:
            return DfAssetbalance().query_df(None, None)
        return super().df_info()

    def df_income(self, quarter_start, quarter_end):
        if IS_USE_CACHE:
            return DfIncome().query_df(quarter_start, quarter_end)
        return super().df_income(quarter_start, quarter_end)

    def df_predict_quarterni(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfPredictQuarterni().query_df(daily_start, daily_end)
        return super().sql_predict_quarterni(daily_start, daily_end)

    def df_fyyoy(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfFyyoy().query_df(daily_start, daily_end)
        return super().df_fyyoy(daily_start, daily_end)

    def df_rf(self):
        if IS_USE_CACHE:
            return DfRf().query_df(None, None)
        return super().df_rf()

    def df_ttm(self, quarter_start, quarter_end):
        if IS_USE_CACHE:
            return DfTtm().query_df(quarter_start, quarter_end)
        return super().df_ttm(quarter_start, quarter_end)

    def df_trade_dt(self):
        if IS_USE_CACHE:
            return DfTradeDt().query_df(None, None)
        return super().df_trade_dt()

    def df_cashflow(self, quarter_start, quarter_end):
        if IS_USE_CACHE:
            return DfCashflow().query_df(quarter_start, quarter_end)
        return super().df_cashflow(quarter_start, quarter_end)

    def df_indus(self):
        if IS_USE_CACHE:
            return DfIndus().query_df(None, None)
        return super().df_indus()

    def df_national(self):
        if IS_USE_CACHE:
            return DfNational().query_df(None, None)
        return super().df_national()

    def df_shibor(self):
        if IS_USE_CACHE:
            return DfShibor().query_df(None, None)
        return super().df_shibor()

    def df_ashare(self):
        if IS_USE_CACHE:
            return DfAshare().query_df(None, None)
        return super().df_ashare()

    def df_consensus(self, daily_start, daily_end):
        if IS_USE_CACHE:
            return DfConsensus().query_df(daily_start, daily_end)
        return super().df_consensus(daily_start, daily_end)
