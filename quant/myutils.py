#!/usr/bin/python
# coding: UTF-8

"""
This script parse stock info
"""
import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import getopt,argparse

import os
import time
import sys
from datetime import datetime, timedelta,date


def better_possition(win  = 10000, loss = 5000, rate_win = 0.6):
	if loss != 0:
		win_loss_ratio = win/loss
	else:
		win_loss_ratio = 2
	if ((win_loss_ratio >0 ) & (rate_win <=1) & (rate_win > 0)):
		return (rate_win * win_loss_ratio - (1-rate_win)) / win_loss_ratio
	else:
		return 0.2

def n_days_ago(n):
	#now=datetime.now()
	today=date.today()
	#print("Now:\n"+str(today))
	ndays_ago=today-timedelta(n)
	#print(str(n)+" days ago:\n"+str(ndays_ago))
	return str(ndays_ago)

def get_all_price(code_list):
	df = ts.get_realtime_quotes(code_list)
	_length=len(df.name)
	_volume=df.volume
	_amount=df.amount
	_price=df.price
	_low = df.low
	_high = df.high
	_open=df.open
	_bid=df.bid
	idx=_length
	_pre_close=df.pre_close
	_average=np.zeros(_length)
	_range=np.zeros(_length)
	_percentage=np.zeros(_length)
	_Amount=np.zeros(_length)
	while(idx>0):
		idx -=1
		#print(_volume[idx])
		if((float(_volume[idx])!=0)&(float(_low[idx])!=0)&(float(_pre_close[idx])!=0)):
			_average[idx]=float(_amount[idx])/float(_volume[idx])
			_range[idx]=float(_high[idx])/float(_low[idx])-1.0
			_percentage[idx]=float(_price[idx])/float(_pre_close[idx])-1.0
			_Amount[idx]=float(_amount[idx])/100000000.0
	df['average']=_average
	df['range']=_range
	df['percentage']=_percentage
	df['Amount']=_Amount
	df.insert(0,'Name',df.pop('name'))
	df.insert(1,'Code',df.pop('code'))
	df.insert(2,'Price',df.pop('price'))
	df.insert(3,'Pre_close',df.pop('pre_close'))
	df.insert(4,'High',df.pop('high'))
	df.insert(5,'Low',df.pop('low'))
	df.insert(6,'Percentage',df.pop('percentage'))
	df.insert(7,'Range',df.pop('range'))
	df.insert(8,'Average',df.pop('average'))
	df.insert(9,'Amount',df.pop('Amount'))
	df.insert(10,'Time',df.pop('time'))
	#print('='*20)
	#print (df.iloc[:,1:11])
	df.sort_values(by='Percentage', ascending=False, inplace=True)

	pd.set_option('display.width', 200)
	pd.set_option('max_columns',40)
	
	df.sort_values(by='Amount', ascending=False, inplace=True)
	print('='*120)
	print (df.iloc[:10,1:11])
	print('='*120)


def getStockList(stock_list):
	STOCK = ["002281","600487","600522","000413","000009","002230","603337",
	"002241","000292","000839","300024","300134","002074","300236","600198",
	"002253","300166","300078","600435","600703"]
	#Get list from text files
	try:
		f = open(stock_list)
		lines=f.readlines()
		for line in lines:
			if line[0:6] not in STOCK:
				#print(line)
				STOCK.append(line[0:6])
		f.close()
	except IOError:
		print("Can't open the file", stock_list)
	return STOCK

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
	if len(df2.code)==0:
		print ("There was no big order")
	else:
		#print(df2)
		print('='*100)
		print ("Sorting by Abs Ascending:")
		print('='*100)
		df2.insert(0,'Code',df2.code)
		df2.insert(1,'Name',df2.name)
		df2.insert(2,'Buy',df2.buy)
		df2.insert(3,'Sell',df2.sell)
		#df2.insert(4,'YYY',df2.abs)
		print (df2.iloc[:50,:5])

		print ("Sorting by ABS descending:")
		print('='*100)
		df2.sort_values(by='Abs', ascending=True, inplace=True)
		print (df2.iloc[:50,:5])

		print ("Sorting by Buy Orders")
		print('='*100)
		df2.sort_values(by='Buy', ascending=False, inplace=True)
		print (df2.iloc[:50,:5])

		print ("Sorting by Sell Orders\n")
		print('='*100)
		df2.sort_values(by='Sell', ascending=False, inplace=True)
		print (df2.iloc[:50,:5])

def getDataUpdate (stock_selected,date,volume):
	df = ts.get_sina_dd(stock_selected,date,vol=volume)
	_time=['9:25:0']
	_volume=[0]
	_price=[0]
	all_time=[]
	all_volume=[]
	all_price=[]
	buy_time=[]
	buy_volume=[]
	buy_price=[]
	sell_time=[]
	sell_volume=[]
	sell_price=[]
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
			buy_price.append(df.price[idx])
			_time.append(df.time[idx])
			_volume.append(df.volume[idx])
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			_price.append(df.price[idx])
			all_time.append(df.time[idx])
			all_volume.append(df.volume[idx])
			all_price.append(df.price[idx])
			#_buy += float(df.volume[idx])*float(df.price[idx])/10000.0
		elif(df.type[idx] == "卖盘"):
			i=i+1
			sell_time.append(df.time[idx])
			sell_volume.append(0-df.volume[idx])
			sell_price.append(df.price[idx])
			_time.append(df.time[idx])
			_volume.append(0-float(df.volume[idx]))
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			_price.append(df.price[idx])
			all_time.append(df.time[idx])
			all_volume.append(0-float(df.volume[idx]))
			all_price.append(df.price[idx])
	df1=pd.DataFrame({'time':_time,'volume':_volume,'price':_price})
	df2=pd.DataFrame({'time':all_time,'volume':all_volume,'price':all_price})
	#print(df2)
	df3=pd.DataFrame({'time':buy_time,'volume':buy_volume,'price':buy_price})
	df4=pd.DataFrame({'time':sell_time,'volume':sell_volume,'price':sell_price})
	return df1,df2,df3,df4

def get_big_order_data (stock_selected,date,volume):
	df = ts.get_sina_dd(stock_selected,date,vol=volume)
	_time=['9:25:0']
	_volume=[0]
	_price=[0]
	all_time=[]
	all_volume=[]
	all_price=[]
	buy_time=[]
	buy_volume=[]
	buy_price=[]
	sell_time=[]
	sell_volume=[]
	sell_price=[]
	if df is None:
		idx=0
	else:
		idx=len(df.time)
	i=0
	while(idx>0):
		idx -=1
		if(df.type[idx] == "买盘"):
			i=i+1
			buy_time.append(date+" " + df.time[idx])
			buy_volume.append(df.volume[idx])
			buy_price.append(df.price[idx])
			_time.append(date+" " + df.time[idx])
			_volume.append(df.volume[idx])
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			_price.append(df.price[idx])
			all_time.append(date+" " + df.time[idx])
			all_volume.append(df.volume[idx])
			all_price.append(df.price[idx])
			#_buy += float(df.volume[idx])*float(df.price[idx])/10000.0
		elif(df.type[idx] == "卖盘"):
			i=i+1
			sell_time.append(date+" " + df.time[idx])
			sell_volume.append(0-df.volume[idx])
			sell_price.append(df.price[idx])
			_time.append(date+" " + df.time[idx])
			_volume.append(0-float(df.volume[idx]))
			_volume[i]=float(_volume[i])+float(_volume[i-1])
			_price.append(df.price[idx])
			all_time.append(date+" " + df.time[idx])
			all_volume.append(0-float(df.volume[idx]))
			all_price.append(df.price[idx])
	df1=pd.DataFrame({'time':_time,'volume':_volume,'price':_price})
	df2=pd.DataFrame({'time':all_time,'volume':all_volume,'price':all_price})
	#print(df2)
	df3=pd.DataFrame({'time':buy_time,'volume':buy_volume,'price':buy_price})
	df4=pd.DataFrame({'time':sell_time,'volume':sell_volume,'price':sell_price})
	return df,df1,df2,df3,df4

def usage():
	print (sys.argv[0] + ' -i stock list file')
	print (sys.argv[0] + ' -h get help info')
	print (sys.argv[0] + ' -a check all list')
	print (sys.argv[0] + ' -s stock id')
	

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "ti:o:v:d:s:", ["help", "input=", "output="])
	stock_list=''
	single_stock=False
	stock_selected="002281"
	for op, value in opts:
		if op == '-i':
			stock_list=value
		elif op == '-a':
			stock_list='all.txt'
		elif op == '-s':
			single_stock=True
			stock_selected = value
		elif op == '-h':
			usage()
			sys.exit()

	if single_stock == True:
		STOCK_LIST=stock_selected
	else:
		STOCK_LIST=getStockList(stock_list)
	while True:
		try:
			os.system('clear')
			get_all_price(STOCK_LIST)
			time.sleep(15)
		except KeyboardInterrupt as e:
			print('')
			print("BYE-BYE")
			sys.exit(0)

