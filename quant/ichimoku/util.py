"""MLT: Utility code."""

import os
import pandas as pd
import matplotlib.pyplot as plt

import tushare as ts




def get_data(symbols, start,end):
    df=ts.get_k_data(symbols,start,end)
    return df

def plot_data(df1,df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    #ichimoku fill between
    plt.fill_between(df.index, df['spana'], df['spanb'], where=df['spanb'] >= df['spana'], facecolor='red', interpolate=True)
    plt.fill_between(df.index, df['spana'], df['spanb'], where=df['spanb'] <= df['spana'], facecolor='green', interpolate=True)

   
    df2=df1[df.index%25==0]
    plt.grid(True)
    plt.xticks(df2.index, df2['date'])
    plt.show()

