# -*- coding:utf-8 -*-
import jqdatasdk
import chanlib as chan
import time

import getopt,argparse
import datetime as d
import os
import sys



def usage():
	print (sys.argv[0] + ' -i stock list file')
	print (sys.argv[0] + ' -h get help info')
	print (sys.argv[0] + ' -a check all list')
	print (sys.argv[0] + ' -s stock id')


now = int(time.time())#这是时间戳
#转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
timeArray = time.localtime(now)
Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# ================需要修改的参数==============
end_date =  Time #'2017-08-14 15:15:00', 最后生成k线日期

stock_days = 60 # 看几天/分钟前的k线　
x_jizhun = 20 #x轴展示的时间距离  5：日，40:30分钟， 48： 5分钟
stock_frequency = '30m' # 1d日线， 30m 30分钟， 5m 5分钟，1m 1分钟
chanK_flag = True# True 看缠论K线， False 看k线

# Tracking
stock_code = []



if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "h:f:d:s:", ["help", "input=", "output="])
	for op, value in opts:
		if op == '-f':
			stock_frequency = value
		elif op == '-d':
			stock_days=int(value)
		elif op == '-s':
			if value[0] =='6':
				stock_code.append(value+'.XSHG')
			elif value[0] =='0' or value[0] =='3':
				stock_code.append(value+'.XSHE')
		elif op == '-h':
			usage()

	if len(stock_code) == 0:
		stock_code = ['600487.XSHG']
	for st in stock_code:
		chan.run_chan_analysis(st,end_date,stock_days,x_jizhun,stock_frequency,chanK_flag)
