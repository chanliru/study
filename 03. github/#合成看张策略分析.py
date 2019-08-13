#合成看张策略分析
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lib.qiquan import*
###########################################################################################
#读取50etf标的
df=pd.read_excel('50etf_fund.xlsx')
df.index=df['tradeDate']
#获取交易日期
date=list(df['tradeDate'])
####################################################################
profit=[]
for i in range(1,len(date)):  
        day=date[i]
        etf_price_close=float(df[df['tradeDate'].isin([day])]['close'])
        etf_price_open=float(df[df['tradeDate'].isin([day])]['open'])
        secID_data_low=list(get_low(df,day)['secID'])
        #print data
        #获取近月代码
        near_c_low=secID_data_low[-2]
        near_p_low=secID_data_low[-1] 
        #####
        secID_data_high=list(get_high(df,day)['secID'])
        #print data
        #获取近月代码
        near_c_high=secID_data_high[-2]
        near_p_high=secID_data_high[-1] 
        #获取近月价格
        option_c_data_low=DataAPI.MktOptdGet(tradeDate=day,
                                           secID=near_c_low,optID=u"",ticker=u"",beginDate=u"",endDate=u"",field=u"",pandas="1")
 
        option_p_data_low=DataAPI.MktOptdGet(tradeDate=day,secID=near_p_low,
                                             optID=u"",ticker=u"",beginDate=u"",endDate=u"",field=u"",pandas="1")
        option_c_data_high=DataAPI.MktOptdGet(tradeDate=day,
                                           secID=near_c_high,optID=u"",ticker=u"",beginDate=u"",endDate=u"",field=u"",pandas="1")
 
        option_p_data_high=DataAPI.MktOptdGet(tradeDate=day,secID=near_p_high,
                                             optID=u"",ticker=u"",beginDate=u"",endDate=u"",field=u"",pandas="1")
        buy_condition=get_up(df,date,i,20)
        #print buy_condition
        if buy_condition==False:
            money=(-etf_price_close+etf_price_open+float(option_c_data_high['closePrice'])-float(option_c_data_high['openPrice']))*10000
            profit.append(money)
        if buy_condition==True:
            money=(float(option_p_data_low['closePrice'])-float(option_p_data_low['openPrice'])+etf_price_close-etf_price_open)*10000
            profit.append(money)
all_profit=pd.Series(profit).cumsum()