import pandas as pd
import numpy as np
import os
#from ta import ichimoku
from util import get_data, plot_data

from pandas import DataFrame, Series
from technical_analysis import ichimoku
from datetime import datetime, timedelta,date
import os
import time
import sys
import getopt,argparse


def test_run(stock='000725'):

	duration = 360
	#now=datetime.now()
	today=date.today()
	ndays_ago=today-timedelta(duration)
	#print(str(n)+" days ago:\n"+str(ndays_ago))
	start_date=str(ndays_ago)
	end_date =str(today)


	df = get_data(stock,start_date, end_date)
	plot_data(df,ichimoku(df['close']),title=stock)


def usage():
	print (sys.argv[0] + ' -s stock id')
	

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "s:")
	stock_list=''
	single_stock=False
	stock_selected="002281"
	for op, value in opts:
		if op == '-s':
			stock_selected = value
		elif op == '-h':
			usage()
			sys.exit()
	
	test_run(stock_selected)