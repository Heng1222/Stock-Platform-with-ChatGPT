# -*- coding:utf-8 -*-
from data import getData, backTest, getStockList, getReadStockList
from Chart import ChartCandle,ChartTrade,Performance, getMaLine
from storage import deleteAllfile #deleteAllfile("todayResult/")
from stastic import Stastic
import pandas as pd
from datetime import date
import mplfinance as mpf
import json
import sys
import traceback
# 取得KD指標
from ta.momentum import StochasticOscillator
boolExpression =" ".join(sys.argv[1:])
# 清除之前數據
deleteAllfile("todayResult/")

today = date.today().isoformat() #今天日期

#取得愈篩選的股票清單
stock_list = getReadStockList()[200:400]
# print(stock_list)

#回測數據Json
Performance_list = []
try:
    for prod, name in stock_list.values:
        data=getData(prod, '2023-01-01', today)
        addp = [] #副圖array
        # 取得ma線
        addp.extend(getMaLine(data))
        #前高低價
        data['ceil'] = data.rolling(20)['high'].max().shift() #5天最高價
        data['floor'] = data.rolling(20)['low'].min().shift() #10天最價
        # print(data.rolling(20)['ceil'].apply(fun))
        # data['ceil2'] = data.rolling(5)['close'].apply(lambda x: pd.Series(x).nlargest(2).iloc[-1])#次高價
        # addp.append(mpf.make_addplot(data['ceil'], color='#0000FF', width=0.5))
        # addp.append(mpf.make_addplot(data['floor'], color='#0000FF', width=0.5))
        # KD指標
        stoch = StochasticOscillator(high=data['high'], low=data['low'], close=data['close'], n=9, d_n=3) #14,3
        data['K'] = stoch.stoch()
        data['D'] = stoch.stoch_signal()
        data['D5mean'] = data.rolling(5)['D'].mean().shift()
        addp.append(mpf.make_addplot(data['K'], color='#F2643D', width=1.5, panel = 1))
        addp.append(mpf.make_addplot(data['D'], color='#3D4FF2', width=1.5, panel = 1))
        
        # 近三日基本數據
        c_time = data.index[-20:]
        volume = data.loc[c_time, 'volume']
        c_low = data.loc[c_time, 'low']
        c_high = data.loc[c_time, 'high']
        c_close = data.loc[c_time, 'close']
        c_open = data.loc[c_time, 'open']
        ma5 = data.loc[c_time, '5ma']
        ma10 = data.loc[c_time, '10ma']
        ma20 = data.loc[c_time, '20ma']
        ceil = data.loc[c_time, 'ceil']
        floor = data.loc[c_time, 'floor']
        K = data.loc[c_time,"K"]
        D = data.loc[c_time, "D"]
        D5mean = data.loc[c_time, "D5mean"]
        if (eval(boolExpression)):
            #回測交易邏輯
            trade = backTest(data, prod, boolExpression)
            # 預言家模型未來股票預測
            predict = Stastic(data,today + " " + prod)
            #畫圖  
            # print(data.columns)
            ChartTrade(data, today + " " + prod, trade, addp = addp)
            #回測結果計算並回傳放入list儲存
            Performance_list.append(Performance(today, prod, name, boolExpression, c_close[2], c_open[2], predict, trade))

except Exception as e:
    print(boolExpression)
    with open("todayResult/ErrorMessage.txt", "w") as ErrorMsg:
        ErrorMsg.write(traceback.format_exc())
        ErrorMsg.write("boolExpression = "+boolExpression)
        
        with open("todayResult/Performance_list.json", "w") as outfile: 
            json.dump(Performance_list, outfile)
# 將回測結果存成Json
with open("todayResult/Performance_list.json", "w") as outfile: 
    json.dump(Performance_list, outfile)
    print("SUCCESS")
