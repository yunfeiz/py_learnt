# 1) curve of big order by 30m, 60m, dayly
# 2) Alert at threshold 
# 3) list possible watch list


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
	opts, args = getopt.getopt(sys.argv[1:], "t:i:o:v:d:s:", ["help", "input=", "output="])
	stock_list= '.\stock.txt'
	date='2017-05-19'
	volume=800
	single_stock=False
	for op, value in opts:
		if op == '-i':
			stock_list = value
		elif op == '-t':
			#date=n_days_ago(float(value))
			n=float(value)
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
		df1,df2,df3,df4=get_big_order_data(stock_selected,n,volume)
		print(df1)

		df1.to_csv("data.csv")

		if len(df2.volume)==0:
			print ("There was no big order")
			sys.exit()
		

		fig = plt.figure(figsize=(9.8,6.18))

		ax0 = fig.add_subplot(3,1,1, ylim=(min(df1.price[1:]), max(df1.price[1:])))
		ax0.set_title('Real Time Price')
		ax0.grid(True)


		ax1 = fig.add_subplot(3,1,2, ylim=(min(df1.volume), max(df1.volume)))
		ax1.set_title('Net Volume of Big Order')
		ax1.grid(True)

		if min(df2.volume)+ max(df2.volume) >0:
			ax2 = fig.add_subplot(3,1,3, ylim=(0-max(df2.volume), max(df2.volume)))
		else:
			ax2 = fig.add_subplot(3,1,3, ylim=(min(df2.volume), 0-min(df2.volume)))
		ax2.set_title('Buy/Sell Volume of Big Order')
		ax2.grid(True)


		line0, = ax0.plot_date(df1.time[1:], df1.price[1:], '-',lw=2)
		line0.set_color('red')

		line1, = ax1.plot_date(df1.time, df1.volume, '-',lw=2)
		line1.set_color('red')



		line2, = ax2.plot_date(df3.time, df3.volume, lw=2)
		line2.set_color('red')

		line3, = ax2.plot_date(df4.time, df4.volume, lw=2)
		line3.set_color('green')
	
		plt.show() 



