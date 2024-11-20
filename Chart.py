import mplfinance as mpf
import matplotlib
import pandas as pd
import json
# K棒圖
def ChartCandle(data, addp=[]):
    mcolor = mpf.make_marketcolors(up = 'r', down = 'g', inherit = True) #K棒顏色
    mystyle = mpf.make_mpf_style(base_mpf_style = 'yahoo', marketcolors = mcolor) #加入風格
    mpf.plot(data, style= mystyle, addplot = addp, type = 'candle', volume = True)

# K棒圖+交易紀錄
def ChartTrade(data, title, trade = pd.DataFrame(), addp=[], v_enable = True):
    addp = addp.copy() #複製一份不要動到原本的
    data1 = data.copy()#複製一份不要動到原本的
    #有交易紀錄
    if(trade.shape[0] > 0):
        trade1 = trade.copy() #複製一份不要動到原本的
        #取出入場紀錄
        buy_order_trade = trade1[[2,3]]
        buy_order_trade = buy_order_trade.set_index(2)
        buy_order_trade.columns = ['buy_order']
        buy_order_trade = buy_order_trade.drop_duplicates()
        #取出出場紀錄
        buy_cover_trade = trade1[[6,5]]
        buy_cover_trade = buy_cover_trade.set_index(6)
        buy_cover_trade.columns = ['buy_cover']
        buy_cover_trade = buy_cover_trade.drop_duplicates()
        #將交易紀錄與K線資料彙整
        data1 = pd.concat([data1, buy_order_trade, buy_cover_trade], axis=1)
        # print(data1)
        #將交易紀錄透過副圖的方式畫出
        addp.insert(0,mpf.make_addplot(data1['buy_order'], type = 'scatter', color='#F54733', marker = '^', markersize = 80))
        addp.insert(0,mpf.make_addplot(data1['buy_cover'], type = 'scatter', color = '#000000', marker ='v', markersize = 80))

    #繪製圖表 
    matplotlib.use('agg')
    mcolor = mpf.make_marketcolors(up = 'r', down = 'g', inherit = True) #K棒顏色
    mystyle = mpf.make_mpf_style(base_mpf_style = 'yahoo', rc={'font.size':16, "figure.facecolor": (0.0, 0.0, 0.0, 0),"axes.facecolor":(0.0, 0.0, 0.0, 0)}, marketcolors = mcolor) #加入風格
    # print(title)
    mpf.plot(data1, style= mystyle, addplot = addp, type = 'candle', volume = v_enable, title = "歷史回測結果", scale_padding={'left': 1, 'top': 5, 'right': 2, 'bottom': 0}, tight_layout=True, savefig="todayResult/"+title+".png")


#計算MA線
def getMaLine(data):
    addp = []
    if data.shape[0]>5:
        #5MA線
        data['5ma'] = data.rolling(5)['close'].mean().shift().round(4)
        addp.append(mpf.make_addplot(data['5ma'], color='#53E8F4', width=1))
    if data.shape[0]>10:
        #10MA線
        data['10ma'] = data.rolling(10)['close'].mean().shift().round(4)
        addp.append(mpf.make_addplot(data['10ma'],  color='#5DF565', width=1))
    if data.shape[0]>20:
        #20MA線
        data['20ma'] = data.rolling(20)['close'].mean().shift().round(4)
        addp.append(mpf.make_addplot(data['20ma'],  color='#F5A95D', width=1))
    # if data.shape[0]>60:
    #     #60MA線
    #     data['60ma'] = data.rolling(60)['close'].mean().shift().round(4)
    #     addp.append(mpf.make_addplot(data['60ma'],  color='#F55DA3', width=2, ))
    return addp


def Performance(today, prod, name, strategy, c_close, c_open,predict, trade = pd.DataFrame(), prodtype = 'Stock'):
    # 取得圖片位置
    imagepath = "todayResult/"+today + " " + prod+".png"
    #如果沒有交易議紀錄則不做運算
    if trade.shape[0] == 0:
        # print("沒有交易紀錄")
        P_dict = {"predictimg": predict,"image":imagepath, "標的代號":prod, "公司名稱":name, "分析日期":today, "最後收盤價":c_close, "最後開盤價":c_open, "交易次數" :"沒有交易紀錄", "篩選策略" :strategy}
        return P_dict
    # 建立字典基本資料
    P_dict = {"predictimg": predict, "image":imagepath, "標的代號":prod, "公司名稱":name, "分析日期":today, "最後收盤價":c_close, "最後開盤價":c_open}
    # 基本資訊
    # print(today.center(20,"-"))
    # print((prod+name).center(20,"-"))

    #交易成本 手續費0.1425%*2*券商打折
    if prodtype == 'ETF':
        cost  = 0.001+0.00285 #稅金0.001+手續
    elif prodtype == 'Stock':
        cost = 0.003+0.00285#股票稅金0.003+手續
    else:
        return False
    
    #複製原來的資料，不影響原本
    trade1 = trade.copy()
    trade1.sort_values(2)
    trade1 = trade1.reset_index(drop=True)
    trade1.columns = ['product', 'bs', 'order_time1', 'order_price', 'order_time', 'cover_price', 'cover_time']
    #計算每筆報酬
    trade1['ret'] = (trade1['cover_price'] - trade1['order_price'])/trade1['order_price']-cost
    #計算總報酬
    P_dict["總報酬率"] = (trade1['ret'].sum().round(4))
    # print("總報酬率 %s" %(trade1['ret'].sum().round(4)))
    #交易次數
    P_dict["交易次數"] = trade1.shape[0]
    # print("交易次數 %s" %(trade1.shape[0]))
    #計算平均報酬
    P_dict["平均報酬"] = trade1['ret'].mean().round(4)
    # print("平均報酬%s" %(trade1['ret'].mean().round(4)))
    #平均持有時間
    earn_trade = trade1[trade1['ret']>0]
    loss_trade = trade1[trade1['ret']<=0]
    #判斷是否獲利虧損都有績效，若否則特定輸出
    if(earn_trade.shape[0] == 0):
        # print("交易樣本不足(樣本需有賺有賠)")
        P_dict["平均勝率"] = 0
        P_dict["平均獲利"] = 0
        P_dict["平均虧損"] = loss_trade['ret'].mean().round(4)
        P_dict["期望值"] = None
        P_dict["平均獲利持有天數"] = None
        P_dict["平均虧損持有天數"] = (loss_trade['cover_time'] - loss_trade['order_time']).mean().days
        P_dict["篩選策略"] = strategy
        return P_dict
    elif(loss_trade.shape[0] == 0):
        # print("交易樣本不足(樣本需有賺有賠)")
        P_dict["平均勝率"] = 1
        P_dict["平均獲利"] = earn_trade['ret'].mean().round(4)
        P_dict["平均虧損"] = None
        P_dict["期望值"] = None
        P_dict["平均獲利持有天數"] = (earn_trade['cover_time'] - earn_trade['order_time']).mean().days
        P_dict["平均虧損持有天數"] = None
        P_dict["篩選策略"] = strategy
        return P_dict
    #勝率
    earn_ratio = earn_trade.shape[0]/ trade1.shape[0]
    P_dict["平均勝率"] = earn_ratio
    # print("平均勝率%s" %earn_ratio)
    #平均獲利
    avg_earn = earn_trade['ret'].mean().round(4)
    P_dict["平均獲利"] = avg_earn
    # print("平均獲利%s" % avg_earn)
    #平均虧損
    avg_loss = loss_trade['ret'].mean().round(4)
    P_dict["平均虧損"] = avg_loss
    # print("平均虧損%s" % avg_loss)
    #賺賠比
    odds = abs(avg_earn / avg_loss)
    #期望值
    P_dict["期望值"] = (earn_ratio*odds - (1-earn_ratio)).round(4)
    # print("期望值 %s" %(earn_ratio*odds - (1-earn_ratio)).round(4))
    #平均獲利持有天數
    earn_onopen_day = (earn_trade['cover_time'] - earn_trade['order_time']).mean()
    P_dict["平均獲利持有天數"] = earn_onopen_day.days
    # print("平均獲利持有天數%s" % earn_onopen_day.days)
    #平均虧損持有天數
    loss_onopen_day = (loss_trade['cover_time'] - loss_trade['order_time']).mean()
    P_dict["平均虧損持有天數"] = loss_onopen_day.days
    # print("平均虧損持有天數%s" % loss_onopen_day.days)
    # 補上篩選策略
    P_dict["篩選策略"] = strategy
    return P_dict