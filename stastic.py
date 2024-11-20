import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from stocker import Stocker
def Stastic_v1(data):
    data = data.copy() #複製一份不要動到原本的
    # d_x = data.loc[data.index[:-1],["high", "low", "open", "close"]]
    # d_y = data.loc[data.index[1:],["open"]]
    # x=d_x.to_numpy()
    # y=d_y.to_numpy()
    # ### 訓練/測試的資料分割，以前 80% 的天數資料做訓練，後 20% 來做測試
    # num_data = d_x.shape[0]
    # split_ratio = 0.8
    # ind_split = int(split_ratio * num_data)
    # #
    # x_train = x[:ind_split]
    # y_train = y[:ind_split].reshape(-1,1)
    # # print(x_train, y_train, sep="\n===========\n")
    # x_test = x[ind_split:]
    # y_test = y[ind_split:].reshape(-1,1)
    # split_time = d_x.index[ind_split]
    # # 建立線性迴歸模型
    # ### 訓練模型
    # reg_linear = LinearRegression()
    # reg_linear.fit(x_train, y_train)

    # # ### 將訓練好的模型，用來做預測
    # trainings = reg_linear.predict(x_train).reshape(-1,1)
    # predictions = reg_linear.predict(x_test).reshape(-1,1)
    # future = reg_linear.predict()
    # # ### 將預測結果合在一起
    # all_pred = np.concatenate((trainings, predictions), axis=0)
    # # ### 計算方均根差
    # # train_rmse = np.sqrt(1/x_train.shape[0]*np.squeeze(np.dot((trainings - y_train).T, (trainings - y_train))))
    # # test_rmse = np.sqrt(1/X_test.shape[0]*np.squeeze(np.dot((predictions - y_test).T, (predictions - y_test))))

    # # print("Training RMSE is: %f" % train_rmse)
    # # print("Testing RMSE is: %f" % test_rmse)
    # ### 將預測和真實的股價，放進 df_linear 以便做圖
    # df_linear = pd.DataFrame(all_pred, columns=['Linear'], index=d_y.index)
    # df_linear.loc[data.index[0]] = data.loc[data.index[0], 'close']
    # df_linear=df_linear.sort_index()
    # # print(df_linear.index)
    # # df_linear[data.index[0]]=x[3]
    # # df_linear[data.index[-1]] = y
    # return df_linear
    # # ### 畫出結果
    # df_linear.plot(title="date", grid=True, legend=True, color=['r','C0'])
    # plt.axvline(pd.Timestamp(split_time),color='orange')
    # print(all_pred)
    pass
def Stastic(data, title):
    title = title+"_predict.png"
    data =data.copy()
    # 以收盤價為預測對象
    d_x = data.loc[data.index[:],'close'] 
    Datamodel = Stocker(d_x)
    imgAddress = Datamodel.changepoint_prior_analysis(title = title, changepoint_priors=[0.05])
    return imgAddress