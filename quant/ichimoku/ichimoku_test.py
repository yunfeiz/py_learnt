import pandas as pd
import numpy as np
import os
#from ta import ichimoku
from util import get_data, plot_data

from pandas import DataFrame, Series
from technical_analysis import ichimoku
from datetime import datetime, timedelta,date


def test_run():

	duration = 360
	#now=datetime.now()
	today=date.today()
	ndays_ago=today-timedelta(duration)
	#print(str(n)+" days ago:\n"+str(ndays_ago))
	start_date=str(ndays_ago)
	end_date =str(today)
	stock='000725'

	df = get_data(stock,start_date, end_date)
	plot_data(ichimoku(df))


if __name__ == "__main__":
	test_run()