#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
import math
import scipy.stats
import time
import random
import mail

def loadcsv_add_clear():

	filename='C:/Program Files (x86)/MetaTrader 4/MQL4/Files/price_record.csv'
	file_object = open(filename,'w')
	file_object.write("")
	file_object.close()
	filename='C:/Program Files (x86)/MetaTrader 4/MQL4/Files/tick.csv'
	file_object = open(filename,'w')
	file_object.write("")
	file_object.close()

										
if __name__ == "__main__":
	#write_API("GBPUSD","USDCHF",-0.24836,-0.401,"33133333333333")
	# conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# cur_stock=conn.cursor()
	# cur_action=conn.cursor()
	# cur_result=conn.cursor()
	# cur_d=conn.cursor()
	# cur_check=conn.cursor()
	# cur_result_DB=conn.cursor()
	# cur_stock_releation=conn.cursor()
	# releation_mid(100)
	loadcsv_add_clear()