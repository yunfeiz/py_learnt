# coding=utf-8
import tushare as ts
import matplotlib.finance as mpf
import matplotlib.pyplot as plt
import datetime
from matplotlib.pylab import date2num


def drawKFig(quote_code, start_date, end_date):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
   
    data_list = []
    
    hist_data = ts.get_hist_data(quote_code, start=start_date, end=end_date)  
    for date, row in hist_data.iterrows():
       
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        t = date2num(date_time)
        open, high, close, low,volume = row[:5]
        datas = (t, open, high, low, close,volume/1000000)
        print(volume/10000)
        data_list.append(datas)
     
   
    #fig, ax1 = plt.subplots()
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    #fig.subplots_adjust(bottom=0.2)


    
    ax1.xaxis_date()
    ax2.xaxis_date()
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title(u"Code：" + quote_code)
    plt.xlabel(u"Date")
    plt.ylabel(u"Price")
    mpf.candlestick_ohlc(ax1, data_list, width=2, colorup='red', colordown='green')
    #mpf.volume_overlay3(ax2, data_list, colorup='red', colordown='green', width=4)
    ax1.autoscale_view()
    ax2.autoscale_view()
    plt.grid()
    plt.show()
    pass

if __name__ == "__main__":
    drawKFig(quote_code='000413', start_date='2017-01-08', end_date='2017-06-13')
    