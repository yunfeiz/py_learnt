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
  
from matplotlib import animation   


def analyze_big_order(code_list,date,volume):
	_code_list=[]
	_name_list=[]
	_buy_list=[]
	_sell_list=[]
	_abs_list=[]
	
	
	for stock in code_list:
		#print("="*100)
		_buy=0;
		_sell=0;
		df = ts.get_sina_dd(stock,date=date,vol=volume)  #code,name,time,volume, preprice, type
		amount_buy=0
		amount_sell=0
		amount_neutral=0
		if df is None:
			#print(stock)
			#print("None")
			idx=0
		else:			
			idx=len(df.name)
			_code_list.append(stock)
		while(idx>0):
			idx -=1
			if(df.type[idx] == "买盘"):
				_buy += float(df.volume[idx])*float(df.price[idx])/10000.0
			if(df.type[idx] == "卖盘"):
				_sell += float(df.volume[idx])*float(df.price[idx])/10000.0

		if df is not None:
			_name_list.append(df.name[0])
			_buy_list.append(_buy)
			_sell_list.append(_sell)
			_abs_list.append(float(_buy)-float(_sell))
	df2=pd.DataFrame({'code':_code_list,'name':_name_list,'buy':_buy_list,'sell':_sell_list,'Abs':_abs_list})
	df2.sort_values(by='Abs', ascending=False, inplace=True)
	pd.set_option('display.width', 200)
	pd.set_option('max_columns',40)
	#print(df2)
	print('='*100)
	print ("Sorting by Buy Orders")
	print('='*100)
	df2.insert(0,'Code',df2.code)
	#df2.insert(1,'Name',df2.name)
	df2.insert(1,'Buy',df2.buy)
	df2.insert(2,'Sell',df2.sell)
	#df2.insert(4,'YYY',df2.abs)
	print (df2.iloc[:20,:3])
	'''
	print ("Sorting by Buy Orders")
	print('='*100)
	df2.sort_values(by='Buy', ascending=False, inplace=True)
	print (df2.iloc[:10,:4])
	
	print ("Sorting by Sell Orders\n")
	print('='*100)
	df2.sort_values(by='Sell', ascending=False, inplace=True)
	print (df2.iloc[:10,:4])
	'''

	

def getStockList(stock_list):
#get stock list:
	STOCK = [
	"600522",
	"002230",
	"600487"
	]
	#Get list from text files
	f = open(stock_list)
	lines=f.readlines()
	for line in lines:
		if line[0:6] not in STOCK:
			#print(line)
			STOCK.append(line[0:6])
	#print(STOCK)
	return STOCK

def getDataUpdate (stock_selected,date,volume):
	df = ts.get_sina_dd(stock_selected,date,vol=volume)
	_time=['9:30:0']
	_volume=[0]
	all_time=[]
	all_volume=[]
	buy_time=[]
	buy_volume=[]
	sell_time=[]
	sell_volume=[]
	if df is None:
		idx=0
	else:			
		idx=len(df.time)
	i=0
	while(idx>0):
		idx -=1
		
		if(df.type[idx] == "买盘"):
			i=i+1
			buy_time.append(df.time[idx])
			buy_volume.append(df.volume[idx])
			_time.append(df.time[idx])
			_volume.append(df.volume[idx])
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			all_time.append(df.time[idx])
			all_volume.append(df.volume[idx])
			#_buy += float(df.volume[idx])*float(df.price[idx])/10000.0
		elif(df.type[idx] == "卖盘"):
			i=i+1
			sell_time.append(df.time[idx])
			sell_volume.append(0-df.volume[idx])
			_time.append(df.time[idx])
			_volume.append(0-float(df.volume[idx]))
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			all_time.append(df.time[idx])
			all_volume.append(0-float(df.volume[idx]))
	df1=pd.DataFrame({'time':_time,'volume':_volume})	
	df2=pd.DataFrame({'time':all_time,'volume':all_volume})
	#print(df2)
	df3=pd.DataFrame({'time':buy_time,'volume':buy_volume})		
	df4=pd.DataFrame({'time':sell_time,'volume':sell_volume})
	return df1,df2,df3,df4

def usage():
	print (sys.argv[0] + ' -i inputfile -o outputfile')
	print (sys.argv[0] + ' -h #get help info')


if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "ti:o:v:d:s:", ["help", "input=", "output="])
	stock_list, output_file = '.\stock.txt', ''  #default stock list
	date='2017-05-19'
	volume=800
	single_stock=False
	for op, value in opts:
		if op == '-i' or op == '--input':
			stock_list = value
		elif op == '-o' or op == '--output':
			output_file = value
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
