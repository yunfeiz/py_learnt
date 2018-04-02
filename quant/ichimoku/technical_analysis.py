import numpy as np
from pandas import DataFrame, Series

def hhv(s, n):
    return Series.rolling(s, n).max()

def llv(s, n):
    return Series.rolling(s, n).min()

    
#ichimoku
def ichimoku(s, n1=9, n2=26, n3=52):

    #average of N-day high and N-day low
    conv = (hhv(s, n1) + llv(s, n1)) / 2

    #mid point of the latest 26 days
    base = (hhv(s, n2) + llv(s, n2)) / 2
    
    #mid-point between the first 2 lines,  and plot 26 periods ahead
    spana = (conv + base) / 2
    
    #mid-point between the 52-period low and  52-period high, and plot 26 periods
    spanb = (hhv(s, n3) + llv(s, n3)) / 2
    
    k = s

    #Lspan is closing price, and plot 26 periods in the past
    return DataFrame(dict(k=k,conv=conv, base=base, spana=spana.shift(n2),
                          spanb=spanb.shift(n2), lspan=s.shift(-n2)))
