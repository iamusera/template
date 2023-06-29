from .GetData import GetSourcesData

date='20190521'
class DataProcess:

    def run(self):
        data=GetSourcesData(date)
        df_list=data.select_stock()
        df_size = data.get_size_data()
        df_beta = data.get_beta_data()
        df_btop = data.get_book_to_price_data()
        df_liquidity = data.get_liquidity_data()
        df_earnings_yield = data.get_earnings_yield_data()
        df_growth = data.get_growth_data()
        df_leverage = data.get_leverage_data()

