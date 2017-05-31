#!/usr/bin/python
# coding: UTF-8

"""
This script parse stock info
"""
import getopt,argparse
import datetime as d
import os
import time

from myutils import *



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

