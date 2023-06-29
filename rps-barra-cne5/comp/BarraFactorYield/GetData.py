import datetime
import pandas as pd
import numpy as np
from application.extensions.init_sqlalchemy import db
from dateutil.relativedelta import relativedelta
import warnings
warnings.filterwarnings("ignore")




class GetSourcesData:

    def __init__(self,date):
        self.date=date
    '''
    入参：日期
    '''


    '''
    筛选样本域
    (1) 对于只有 A 股的上市公司, 退市日期为 A 股退市日期;
    (2) 对于同时有 A 股和 B 股的上市公司, 退市日期取 A 股退市日和 B 股退市日中较早的一个.
    (3) 不考虑北交所
    '''
    def select_stock(self):
        sql='''select  a.S_INFO_WINDCODE,
                       a.S_INFO_LISTDATE,
                       a.S_INFO_DELISTDATE as s_info_delistdate,
                       b.S_INFO_DELISTDATE as bs_info_delistdate
                from AShareDescription a
                left join BShareDescription b
                on a.S_INFO_COMPNAME=b.S_INFO_COMPNAME
                where a.S_INFO_EXCHMARKET!='BSE'    '''
        df_list=pd.read_sql(sql, db.engine)
        df_list.columns=['s_info_windcode','s_info_listdate','s_info_delistdate','bs_info_delistdate']
        df1=df_list.dropna(subset=['s_info_listdate'])
        df1[['s_info_delistdate','bs_info_delistdate']]=df1[['s_info_delistdate','bs_info_delistdate']].fillna(value=self.date)

        stock_list=df1[(df1['s_info_listdate']<=self.date) & (df1['s_info_delistdate']>=self.date) & (df1['bs_info_delistdate']>=self.date)]
        #stock_list=stock_list[stock_list['s_info_listdate']!=stock_list['s_info_delistdate']]#剔除目标日期当日上市的
        stock_universe=stock_list['s_info_windcode']
        stock_list.to_csv('stock_list.csv')
        return stock_universe




    '''
    1、size：当日————普通股总市值，万元;计算公式:A股股价*总股本(包含B股,H股等,除优先股)    ,
    处理：对于缺失值，用上一日填充，鉴于股票停牌一般不超过20交易日，在此取目标日期前推40交易日的数据，采用向后填充，取最后一日截面值。
    '''
    def get_size_data(self):

        sql = f'''
        with
            dt_date as (select TRADE_DAYS from (
                                                   SELECT TRADE_DAYS,ROW_NUMBER()OVER( ORDER BY TRADE_DAYS DESC) as rn FROM winddb.AShareCalendar a
                                                   where a. S_INFO_EXCHMARKET='SSE'
                                                     and a.TRADE_DAYS<='{self.date}'
                                                     )
        where rn=40)
        SELECT S_INFO_WINDCODE,TRADE_DT,S_VAL_MV
        FROM AShareEODDerivativeIndicator
        where TRADE_DT BETWEEN (select TRADE_DAYS from dt_date) AND '{self.date}'
        order by TRADE_DT desc
        '''
        df = pd.read_sql(sql, db.engine)
        df.columns=['s_info_windcode','trade_dt','s_val_mv']
        df1=df[df['s_info_windcode'].isin(self.select_stock())]

        #处理：向后填充，取最后一日
        df2=df1.pivot(index='trade_dt',columns='s_info_windcode',values='s_val_mv')
        df2=df2.fillna(method='ffill')
        df_last=df2.loc[self.date,:]

        df_last.to_csv('df_last.csv')
        return df_last




    '''2、beta：过去252交易日————复权收盘价、wind全A指数收盘价、无风险利率一年期定存%(数据量较少，直接取2008至今的）、样本域全部股票
    处理：收盘价缺失值填充上一日；对于停牌股票，收盘价沿用上一日，使其收益为0'''
    def get_beta_data(self):
        sql_price = f'''
        with
            dt_date as (select TRADE_DAYS from (
                                                   SELECT TRADE_DAYS,ROW_NUMBER()OVER( ORDER BY TRADE_DAYS DESC) as rn FROM winddb.AShareCalendar a
                                                   where a. S_INFO_EXCHMARKET='SSE'
                                                     and a.TRADE_DAYS<='{self.date}'
                                                     )
        where rn=253)
        SELECT  S_DQ_ADJCLOSE,TRADE_DT, S_INFO_WINDCODE
        FROM WINDDB.AShareEODPrices
        where TRADE_DT BETWEEN (select TRADE_DAYS from dt_date) AND '{self.date}'
        order by TRADE_DT desc
        '''
        df_price = pd.read_sql(sql_price, db.engine)


        #目标日期过去252个交易日的wind全A复权收盘价
        sql_index = f'''
        with
            dt_date as (select TRADE_DAYS from (
                                                   SELECT TRADE_DAYS,ROW_NUMBER()OVER( ORDER BY TRADE_DAYS DESC) as rn FROM winddb.AShareCalendar a
                                                   where a. S_INFO_EXCHMARKET='SSE'
                                                     and a.TRADE_DAYS<='{self.date}'
                                                   )
                        where rn=253)
        SELECT  S_DQ_CLOSE,TRADE_DT, S_INFO_WINDCODE
        FROM WINDDB.AIndexWindIndustriesEOD
        where TRADE_DT BETWEEN (select TRADE_DAYS from dt_date) AND '{self.date}'
          AND S_INFO_WINDCODE IN ('881001.WI')
        order by TRADE_DT desc  
        '''
        df_index = pd.read_sql(sql_index, db.engine)

        sql_rf='''select TRADE_DT,B_INFO_RATE from CBondBenchmark where B_INFO_BENCHMARK='01010203' and TRADE_DT>'20070101'  '''
        df_rf=pd.read_sql(sql_rf, db.engine)

        #日期对齐，行情向后填充，rf向后填充，列索引按行情交易日
        df_price=df_price.pivot(index='s_info_windcode',columns='trade_dt',values='s_dq_adjclose')
        df_price=df_price[df_price.index.isin(self.select_stock())]#取出universe
        df_price=df_price.T
        df_price = df_price.fillna(method='ffill').pct_change()
        df_index=df_index.pivot(index='trade_dt',columns='s_info_windcode',values='s_dq_close')
        df_index=df_index.fillna(method='ffill').pct_change()
        df_rf['b_info_rate']=df_rf['b_info_rate']/(365*100)
        df_rf=df_rf.set_index(['trade_dt'],drop=True)

        df_merge1=pd.concat([df_price,df_index],axis=1)
        df_merge2=pd.merge(df_merge1,df_rf,left_index=True,right_index=True,how='outer')
        df_merge2['b_info_rate']=df_merge2['b_info_rate'].fillna(method='ffill')
        df1=df_merge2[df_merge2.index.isin(df_merge1.index)]

        df1.to_csv('df1.csv')

        return df1





    '''3、momentum：过去252交易日————复权收盘价 复用beta中的复权收盘价'''
    '''4、residual_volatility:过去252交易日————个股复权收盘价，无风险利率，复用beta中的数据'''
    '''5、non_linear_size: 当日————总市值，复用size因子的数据'''




    '''
    6、book_to_price：
    最近财报日————普通股账面价值(股东权益合计（含少数股东权益）-优先股-永续债）、
    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————取目标日期，缺失值回归法填充，现在是取的临近值，相当于上一期值填充
    当日————普通股总市值（复用size因子的市值数据）
    '''
    def get_book_to_price_data(self):
        sql_book = f'''
        with 
        max_info as (
            SELECT
                a.s_info_windcode
                ,max(a.REPORT_PERIOD) as REPORT_PERIOD
            FROM WINDDB.AShareBalanceSheet a
            where a.REPORT_PERIOD<='{self.date}'
            GROUP BY a.s_info_windcode)
        SELECT a.S_INFO_WINDCODE,a.REPORT_PERIOD,a.TOT_SHRHLDR_EQY_INCL_MIN_INT,a.OTHER_EQUITY_TOOLS_P_SHR,a.OTHER_SUSTAINABLE_BOND FROM  WINDDB.AShareBalanceSheet a
                   inner JOIN max_info b
                              ON a.s_info_windcode=b.s_info_windcode
                                  AND a.REPORT_PERIOD=b.REPORT_PERIOD
                                  AND a.STATEMENT_TYPE='408001000' 
        '''
        df_book = pd.read_sql(sql_book, db.engine)

        df_book.to_csv('df_book.csv')
        return df_book





    '''7、liquidity：过去12个月————每日交易量(手,后续需转换)、流通股数量(中国A股自由流通股本（万股）)
     处理：交易量为空，填充0；取max(startdate，上市日)至目标日期的交易量，流通股本，startdate=目标日期前推252交易日。流通股本向后填充
          后面单个股票处理，每个个股取上市日至目标日期的数据进行计算，因为成交量数据 和流通股本的日期  在上市日前可能有值（北交所）
    '''
    def get_liquidity_data(self):
        sql_turnover = f'''
        with
            dt_date as (select TRADE_DAYS from (
                                                   SELECT TRADE_DAYS,ROW_NUMBER()OVER( ORDER BY TRADE_DAYS DESC) as rn FROM winddb.AShareCalendar a
                                                   where a. S_INFO_EXCHMARKET='SSE'
                                                     and a.TRADE_DAYS<='{self.date}'
                                                   )
                        where rn=253)
        SELECT  S_INFO_WINDCODE,TRADE_DT,S_DQ_VOLUME
        FROM WINDDB.AShareEODPrices
        where TRADE_DT BETWEEN (select TRADE_DAYS from dt_date) AND '{self.date}'
        order by TRADE_DT desc 
        '''
        df_turnover = pd.read_sql(sql_turnover, db.engine)

        sql_tradable = f'''
        with
            dt_date as (select TRADE_DAYS from (
                                                   SELECT TRADE_DAYS,ROW_NUMBER()OVER( ORDER BY TRADE_DAYS DESC) as rn FROM winddb.AShareCalendar a
                                                   where a. S_INFO_EXCHMARKET='SSE'
                                                     and a.TRADE_DAYS<='{self.date}'
                                                   )
                        where rn=253)
        SELECT  S_INFO_WINDCODE,TRADE_DT,FLOAT_A_SHR_TODAY
        FROM WINDDB.AShareEODDerivativeIndicator
        where TRADE_DT BETWEEN (select TRADE_DAYS from dt_date) AND '{self.date}'
        order by TRADE_DT desc
 
        '''
        df_tradable = pd.read_sql(sql_tradable, db.engine)

        df_turnover = df_turnover.pivot(index='trade_dt', columns='s_info_windcode', values='s_dq_volume')
        df_tradable=df_tradable.pivot(index='trade_dt', columns='s_info_windcode', values='float_a_shr_today')

        df_turnover.to_csv('df_turnover.csv')
        df_tradable.to_csv('df_tradable.csv')

        return df_turnover,df_tradable





    '''8、earnings_yield:分析师一致预期净利润(预测日期，预测报告期)；总市值（复用size的）；现金收入TTM（经营性现金流）;净利润TTM'''
    def get_earnings_yield_data(self):
        #取离现在最近的EST_REPORT_DT
        sql_predict=f'''select 
                        a.S_INFO_COMPCODE
                        ,a.EST_REPORT_DT
                        ,a.NET_PROFIT 
                        ,b.s_info_windcode
                        from WIND.AShareConsensusindex a
                        LEFT JOIN  wind.AShareDescription b
                        ON a.s_info_compcode=b.s_info_compcode
                        AND (b.S_INFO_DELISTDATE>='{self.date}' OR b.S_INFO_DELISTDATE is null)
                        AND b.S_INFO_LISTDATE is not null  '''
        df_predict=pd.read_sql(sql_predict,db.engine)
        #取最近报告期TTM
        sql_ni_cashearnings=f'''
        with 
        max_info as (
            SELECT
                a.s_info_windcode
                ,max(a.REPORT_PERIOD) as REPORT_PERIOD
            FROM WINDDB.AShareBalanceSheet a
            where a.REPORT_PERIOD<='{self.date}'
            GROUP BY a.s_info_windcode)
        SELECT a.S_INFO_WINDCODE,a.REPORT_PERIOD,a.S_FA_PROFIT_TTM,a.S_FA_OPERATECASHFLOW_TTM from WINDDB.AShareTTMAndMRQ a
                   inner JOIN max_info b
                              ON a.s_info_windcode=b.s_info_windcode
                                  AND a.REPORT_PERIOD=b.REPORT_PERIOD
                                  AND a.STATEMENT_TYPE='408001000' 
        '''
        df_ni_cashearnings=pd.read_sql(sql_ni_cashearnings,db.engine)

        df_predict.to_csv('df_predict.csv')
        df_ni_cashearnings.to_csv('df_ni_cashearnings.csv')

        return df_predict,df_ni_cashearnings




    '''9、growth:个股过去5年 总营收、净利润，预测净利润增长率长期（FY3-FY0)/FY0,短期净利润增长率YOY，#根据当前日期和上市日期往前推，个股互不相同'''
    def get_growth_data(self):
        data_start = (pd.to_datetime(self.date) + relativedelta(years= -12)).strftime("%Y%m%d")
        #过去5年总营收 净利润
        sql_revenue_ni=f'''select S_INFO_WINDCODE,REPORT_PERIOD,NET_PROFIT_INCL_MIN_INT_INC,TOT_OPER_REV from AShareIncome where REPORT_PERIOD between '{data_start}' and '{self.date}'  '''
        df_revenue_ni = pd.read_sql(sql_revenue_ni, db.engine)
        #EST_DT为自然日
        sql_forcast=f'''select S_INFO_WINDCODE,NET_PROFIT,EST_DT,ROLLING_TYPE from AShareConsensusRollingData where ROLLING_TYPE in ('FY0','FY3','YOY') and EST_DT='{self.date}'  '''
        df_forcast=pd.read_sql(sql_forcast,db.engine)

        df_revenue_ni.to_csv('df_revenue_ni.csv')
        df_forcast.to_csv('df_forcast.csv')
        return df_revenue_ni,df_forcast



    '''
    10、leverage:总市值(复用size)、优先股与永续债&普通股账面价值(复用btop)，
    取数：长期债务：非流动负债
    流动负债、总资产账面价值直接取
    时点值，取离现在最近的
    '''
    def get_leverage_data(self):
        sql_assets=f'''
         with 
        max_info as (
            SELECT
                a.s_info_windcode
                ,max(a.REPORT_PERIOD) as REPORT_PERIOD
            FROM WINDDB.AShareBalanceSheet a
            where a.REPORT_PERIOD<='{self.date}'
            GROUP BY a.s_info_windcode)
        SELECT a.S_INFO_WINDCODE,a.REPORT_PERIOD,a.TOT_CUR_LIAB,a.TOT_NON_CUR_LIAB,a.TOT_CUR_LIAB,a.TOT_ASSETS from AShareBalanceSheet a
                   inner JOIN max_info b
                              ON a.s_info_windcode=b.s_info_windcode
                                  AND a.REPORT_PERIOD=b.REPORT_PERIOD
                                  AND a.STATEMENT_TYPE='408001000' 
        '''

        df_assets_debt=pd.read_sql(sql_assets_debt,db.engine)

        df_assets_debt.to_csv('df_assets_debt.csv')
        return df_assets_debt




