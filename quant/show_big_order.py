#-*-coding:utf-8-*-
#!/usr/bin/python
# coding: UTF-8

"""
This script parse stock info
"""
import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpdates
import sys,getopt,argparse
import datetime as dt
import time

from myutils import *
from matplotlib import animation




def usage():
	print (sys.argv[0] + ' -i stock list file')
	print (sys.argv[0] + ' -h #get help info')
	print (sys.argv[0] + ' -t show data today')
	print (sys.argv[0] + ' -v threshold, for example 800')
	print (sys.argv[0] + ' -a check all list')
	print (sys.argv[0] + ' -d set date')

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "ti:o:v:d:s:", ["help", "input=", "output="])
	stock_list= '.\stock.txt'
	date='2017-05-19'
	volume=800
	single_stock=False
	for op, value in opts:
		if op == '-i':
			stock_list = value
		elif op == '-t':
			date=dt.date.today()
		elif op == '-d':
			date=value
		elif op == '-v':
			volume=float(value)
		elif op == '-s':
			single_stock=True
			stock_selected = value
		elif op == '-h':
			usage()
			sys.exit()
	
	if single_stock == True:
		df1,df2,df3,df4=getDataUpdate(stock_selected,date,volume)
		print(df2)
		if len(df2.volume)==0:
			print ("There was no big order")
			sys.exit()
		

		fig = plt.figure() 
		ax1 = fig.add_subplot(2,1,1, ylim=(min(df1.volume), max(df1.volume)))
		ax1.set_title('Net volume')
		ax1.grid(True)
		if min(df2.volume)+ max(df2.volume) >0:
			ax2 = fig.add_subplot(2,1,2, ylim=(0-max(df2.volume), max(df2.volume)))
		else:
			ax2 = fig.add_subplot(2,1,2, ylim=(min(df2.volume), 0-min(df2.volume)))
		ax2.set_title('Buy/Sell Volume')
		ax2.grid(True)
		line, = ax1.plot_date(df1.time, df1.volume, '-',lw=2)  
		line2, = ax2.plot_date(df3.time, df3.volume, lw=2)
		line2.set_color('red')
		line3, = ax2.plot_date(df4.time, df4.volume, lw=2)
		line3.set_color('green')
	
		plt.show()
		
	else:
		STOCK_LIST=getStockList(stock_list)	
		analyze_big_order(STOCK_LIST,date,volume)
