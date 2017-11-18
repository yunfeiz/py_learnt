"""MLT: Utility code."""

import os
import pandas as pd
import matplotlib.pyplot as plt

import tushare as ts




def get_data(symbols, start,end):
    df=ts.get_k_data(symbols,start,end)
    #stocks=df.rename(index=str, columns={"date":"Datetime","close":"Close","high":"High","low":"Low","open":"Open","volume":"Volume"}) 
    #df.index=df['date']
    #print(df)
    return df['close']

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    #ichimoku fill between
    print(df.index)

    plt.fill_between(df.index, df['spana'], df['spanb'], where=df['spanb'] >= df['spana'], facecolor='red', interpolate=True)
    plt.fill_between(df.index, df['spana'], df['spanb'], where=df['spanb'] <= df['spana'], facecolor='green', interpolate=True)
    plt.grid(True)
    print(df.index)
    
    #plt.gca().set_color_cycle(['yellowgreen','cyan','black','magenta','green','red'])
    plt.show()

