from application.common.utils.db_dao import DB

class SourcesDataDB:

    def df_windqa(self, daily_start, daily_end):
        sql_windqa = f'''SELECT  S_INFO_WINDCODE,TRADE_DT,S_DQ_CLOSE from WINDDB.AIndexWindIndustriesEOD
        where TRADE_DT BETWEEN '{daily_start}' AND '{daily_end}'
        and S_INFO_WINDCODE='881001.WI'
        order by TRADE_DT desc 
        '''
        return DB.pd_read_sql(sql_windqa)

    def df_otherindex(self, daily_start, daily_end):
        sql_otherindex = f'''SELECT  S_INFO_WINDCODE,TRADE_DT,S_DQ_CLOSE from WINDDB.AIndexEODPrices
        where TRADE_DT BETWEEN '{daily_start}' AND '{daily_end}'
        and S_INFO_WINDCODE in ('000001.SH','000300.SH','000905.SH')
        order by TRADE_DT desc 
        '''
        return DB.pd_read_sql(sql_otherindex)

    def df_volume_share(self, daily_start, daily_end):
        sql_volume_share = f'''SELECT  S_INFO_WINDCODE
        ,TRADE_DT
        ,S_VAL_MV
        ,S_DQ_MV
        ,TOT_SHR_TODAY
        ,FLOAT_A_SHR_TODAY
        from WINDDB.AShareEODDerivativeIndicator
        where TRADE_DT BETWEEN '{daily_start}' AND '{daily_end}'
        order by TRADE_DT desc 
        '''
        return DB.pd_read_sql(sql_volume_share)

    def df_stockprice_tradingvolume(self, daily_start, daily_end):
        sql_stockprice_tradingvolume = f'''SELECT  S_DQ_ADJCLOSE
        ,S_DQ_CLOSE
        ,S_DQ_VOLUME
        ,S_INFO_WINDCODE
        ,TRADE_DT
         from WINDDB.AShareEODPrices
        where TRADE_DT BETWEEN '{daily_start}' AND '{daily_end}'
        order by TRADE_DT desc 
        '''
        return DB.pd_read_sql(sql_stockprice_tradingvolume)

    def df_assetbalance(self, quarter_start, quarter_end):
        sql_assetbalance = f'''SELECT  
        S_INFO_WINDCODE
        ,REPORT_PERIOD
        ,ANN_DT
        ,ACTUAL_ANN_DT
        ,STATEMENT_TYPE
        ,TOT_SHRHLDR_EQY_INCL_MIN_INT
        ,TOT_SHRHLDR_EQY_EXCL_MIN_INT
        ,OTHER_EQUITY_TOOLS_P_SHR
        ,OTHER_SUSTAINABLE_BOND
        ,TOT_ASSETS
        ,TOT_LIAB
        ,TOT_NON_CUR_LIAB
        ,TOT_CUR_LIAB
        ,LT_BORROW
        ,BONDS_PAYABLE
        ,LEASE_LIAB
        from WINDDB.AShareBalanceSheet
        where REPORT_PERIOD BETWEEN '{quarter_start}' AND '{quarter_end}'
        order by ANN_DT desc 
        '''
        # and STATEMENT_TYPE='408001000'
        return DB.pd_read_sql(sql_assetbalance)

    def df_info(self):
        sql_info = '''select 
        a.S_INFO_WINDCODE,
        a.S_INFO_LISTDATE,
        a.S_INFO_EXCHMARKET,
        a.S_INFO_DELISTDATE as s_info_delistdate,
        b.S_INFO_DELISTDATE as bs_info_delistdate
        from AShareDescription a
        left join BShareDescription b
        on a.S_INFO_COMPNAME=b.S_INFO_COMPNAME 
         '''
        return DB.pd_read_sql(sql_info)


    def df_income(self, quarter_start, quarter_end):
        sql_income = f'''SELECT  
        TOT_OPER_REV
        ,NET_PROFIT_EXCL_MIN_INT_INC
        ,NET_PROFIT_INCL_MIN_INT_INC
        ,S_FA_EPS_BASIC
        ,S_FA_EPS_DILUTED
        ,S_INFO_WINDCODE
        ,REPORT_PERIOD
        ,ANN_DT
        ,ACTUAL_ANN_DT
        ,STATEMENT_TYPE
        from WINDDB.AShareIncome
        where REPORT_PERIOD BETWEEN '{quarter_start}' AND '{quarter_end}'
        order by ANN_DT desc 
        '''
        return DB.pd_read_sql(sql_income)

    def pd_predict_quarterni(self, daily_start, daily_end):
        sql_predict_quarterni = f'''select 
        a.S_INFO_COMPCODE
        ,a.EST_REPORT_DT
        ,a.NET_PROFIT 
        ,a.ANN_DT
        ,b.s_info_windcode
        from AShareConsensusindex a
        LEFT JOIN  AShareDescription b
        ON a.s_info_compcode=b.s_info_compcode
        where a.EST_REPORT_DT between '{daily_start}' AND '{daily_end}'
        '''
        return DB.pd_read_sql(sql_predict_quarterni)

    def df_fyyoy(self, daily_start, daily_end):
        sql_fyyoy = f'''select 
        NET_PROFIT
        ,S_INFO_WINDCODE
        ,EST_DT
        ,ROLLING_TYPE
        ,BENCHMARK_YR
        from AShareConsensusRollingData
        where BENCHMARK_YR BETWEEN '{daily_start}' AND '{daily_end}'
        and ROLLING_TYPE in ('FY0','FY3','YOY', 'FTTM')
         '''
        return DB.pd_read_sql(sql_fyyoy)

    def df_rf(self):
        sql_rf = f'''select 
        B_INFO_RATE
        ,B_INFO_BENCHMARK
        ,TRADE_DT
        from CBondBenchmark
        where B_INFO_BENCHMARK='01010203'
        '''
        return DB.pd_read_sql(sql_rf)

    def df_ttm(self, quarter_start, quarter_end):
        sql_ttm = f'''select 
        S_FA_PROFIT_TTM
        ,S_FA_OPERATECASHFLOW_TTM
        ,S_INFO_WINDCODE
        ,REPORT_PERIOD
        ,STATEMENT_TYPE
        from AShareTTMAndMRQ 
        where REPORT_PERIOD BETWEEN '{quarter_start}' AND '{quarter_end}'
        and STATEMENT_TYPE='408001000'

         '''
        return DB.pd_read_sql(sql_ttm)

    def df_trade_dt(self):
        sql_trade_dt = '''SELECT TRADE_DAYS TRADE_DT FROM AShareCalendar where S_INFO_EXCHMARKET='SSE' order by  TRADE_DAYS asc '''
        return DB.pd_read_sql(sql_trade_dt)

    def df_cashflow(self, quarter_start, quarter_end):
        sql_cashflow = f'''SELECT  
        S_INFO_WINDCODE
        ,ANN_DT
        ,REPORT_PERIOD
        ,ACTUAL_ANN_DT
        ,STATEMENT_TYPE
        ,NET_CASH_FLOWS_OPER_ACT
        from WINDDB.AShareCashFlow
        where REPORT_PERIOD BETWEEN '{quarter_start}' AND '{quarter_end}'
        order by ANN_DT desc 
        '''
        return DB.pd_read_sql(sql_cashflow)

    def df_indus(self):
        sql_indus = f'''select
        a.S_INFO_WINDCODE 
        ,a.SW_IND_CODE 
        ,SUBSTR(a.SW_IND_CODE, 1, 4) as induscode
        ,a.ENTRY_DT
        ,a.REMOVE_DT
        ,a.CUR_SIGN 
        ,b.INDUSTRIESNAME from
        AShareSWNIndustriesClass a
        left join AShareIndustriesCode b 
        ON  SUBSTR(a.SW_IND_CODE, 1, 4) =SUBSTR(b.INDUSTRIESCODE, 1, 4)
        where b.LEVELNUM = 2

        '''
        return DB.pd_read_sql(sql_indus)

    def df_national(self):
        sql_national = '''select a.s_info_windcode
        ,a.S_INFO_COMPCODE
        ,b.S_INFO_COMPNAME
        ,a.S_INFO_COUNTRYNAME
        ,a.CRNCY_NAME
        ,a.SECURITY_STATUS
        from WindCustomCode a,AShareDescription b where a.S_INFO_COMPCODE=b.S_INFO_COMPCODE
        '''
        return DB.pd_read_sql(sql_national)

    def df_shibor(self):
        sql_shibor = '''
        select s_info_windcode,trade_dt,b_info_rate,b_info_term 
        from shiborprices where b_info_term='3M' order by trade_dt
        '''
        return DB.pd_read_sql(sql_shibor)

    def df_ashare(self):
        sql_Ashare = '''select
        b.s_info_windcode
        ,b.CHANGE_DT
        ,b.S_SHARE_TOTALA
        from AShareCapitalization b
        order by b.CHANGE_DT  '''
        return DB.pd_read_sql(sql_Ashare)

    def df_consensus(self, daily_start, daily_end):
        sql_consensus = f'''select S_INFO_WINDCODE
        ,EST_DT
        ,EST_REPORT_DT
        ,EPS_AVG
        ,NET_PROFIT_AVG
        ,S_EST_YEARTYPE
        ,CONSEN_DATA_CYCLE_TYP 
        from AShareConsensusData 
        where EST_DT between '{daily_start}' and '{daily_end}'
        order by EST_DT'''
        return DB.pd_read_sql(sql_consensus)
