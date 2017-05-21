#-*-coding:utf-8-*-
# coding: UTF-8

"""
This script parse stock info
"""
import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import sys,getopt,argparse 
import datetime as dt


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
		amount_neutral=stock
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
	if len(df2.Code)==0:
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
	

	

def getStockList(stock_list):
#get stock list:
	STOCK = []
	#Get list from text files
	f = open(stock_list)
	lines=f.readlines()
	for line in lines:
		STOCK.append(line[0:6])
	#print(STOCK)
	return STOCK
	
def usage():
	print (sys.argv[0] + ' -i stock list file')
	print (sys.argv[0] + ' -h #get help info')
	print (sys.argv[0] + ' -t show data today')
	print (sys.argv[0] + ' -v threshold, for example 800')
	print (sys.argv[0] + ' -a check all list')
	print (sys.argv[0] + ' -d set date')



if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "ti:o:v:d:s:a", ["help", "input=", "output="])
	stock_list= '.\stock.txt'
	date='2017-05-19'
	volume=400
	for op, value in opts:
		if op == '-i':
			stock_list = value
		elif op == '-t':
			date=dt.date.today()
		elif op == '-d':
			date=value
		elif op == '-v':
			volume=float(value)
		elif op == '-a':
			stock_list='all.txt'
		elif op == '-h':
			usage()
			sys.exit()
		else:
			usage()
			sys.exit()
	
		
	STOCK_LIST=getStockList(stock_list)	
	analyze_big_order(STOCK_LIST,date,volume)
