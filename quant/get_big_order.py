#-*-coding:utf-8-*-
# coding: UTF-8

"""
This script parse stock info
"""
import pandas as pd
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
from myutils import *
import sys,getopt,argparse 
import datetime as dt


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
