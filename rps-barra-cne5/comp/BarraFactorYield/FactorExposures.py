# from BarraFactorYield.GetData import GetSourcesData
date='20190521'
class FactorExposure:

    def __init__(self,date):
        self.date=date

    # def fetch_data(self):
    #     data=GetSourcesData(self.date)
    #     df_list=data.select_stock()
    #     df_size = data.get_size_data()
    #     df_beta = data.get_beta_data()
    #     df_btop = data.get_book_to_price_data()
    #     df_liquidity = data.get_liquidity_data()
    #     df_earnings_yield = data.get_earnings_yield_data()
    #     df_growth = data.get_growth_data()
    #     df_leverage = data.get_leverage_data()
    #     return data

    def half_life(self,period):
        hl=0.5**(1/period)
        return hl

    def size_exposure(self):
        df_size=pd.read_csv(df_last.csv)
        beta_exposure=np.log(df_size)
        return beta_exposure





