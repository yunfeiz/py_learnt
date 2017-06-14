'''
Created on 2017-5-30
@author: 3xtrees
'''

# coding: UTF-8
import tushare as ts

'''
ma20 strategy
'''
def parse(stock, start_date):  
    '''''process stock'''  
    is_buy = 0
    buy_val = [] 
    buy_date = []
    sell_val = []  
    sell_date = []  
    df = ts.get_hist_data(stock, start=start_date)  
    ma20 = df[u'ma20']  
    close = df[u'close']  
    rate = 1.0  
    idx = len(ma20)
    while idx > 0:  
        idx -= 1
        close_val = close[idx]
        ma20_val = ma20[idx]
        if close_val > ma20_val:
                if is_buy == 0:  
                        is_buy = 1  
                        buy_val.append(close_val)  
                        buy_date.append(close.keys()[idx])  
        elif close_val < ma20_val:  
                if is_buy == 1:  
                        is_buy = 0  
                        sell_val.append(close_val)  
                        sell_date.append(close.keys()[idx])  
  
    print ("stock number: %s" % stock)  
    print ("buy count   : %d" % len(buy_val))  
    print ("sell count  : %d" % len(sell_val)) 
  
    for i in range(len(sell_val)):  
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])  
        print ("buy date : %s, buy price : %.2f" % (buy_date[i], buy_val[i]))  
        print ("sell date: %s, sell price: %.2f" % (sell_date[i], sell_val[i]))  
        
    print ("rate: %.2f" % rate)
    pass

if __name__ == '__main__':    
    stock_pool = ['601668']
    start_date_list = ['2014-05-29', '2015-05-29', '2016-05-29']
    for stock in stock_pool:
        for start_date in start_date_list:
            parse(stock, start_date)