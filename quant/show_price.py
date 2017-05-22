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
import datetime as d
import os
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


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

	
#remove some columns

#reord some colums

	pd.set_option('display.width', 200)
	pd.set_option('max_columns',40)
	#print ("Sorting per Percentage\n")
	#print('='*20)
	#df.drop([df.columns[[10:15]],axis=1,inplace=True)
	#print (df.iloc[:,1:11])
	df.sort_values(by='Amount', ascending=False, inplace=True)
	#print ("Sorting by Amount\n")
	print('='*120)
	#plt.show(df.plot())
	#print(df)
	print (df.iloc[:20,:11])
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
	except:
		print("Can't open the file", stock_list)
	return STOCK

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

