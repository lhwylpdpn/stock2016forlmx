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
import shutil
def getFileList( p ):
	p = str( p )
	if p=="":
		return [ ]
	p = p.replace( "/","\\")
	if p[-1] != "\\":
		p = p+"\\"
	a = os.listdir( p )
	b = [ x   for x in a if os.path.isfile( p + x ) ]
	return b

def load_report():
	s=os.getcwd()
	for filename in getFileList("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order"):
		nameA=[]
		openA=[]
		openA_time=[]
		closeA=[]
		closeA_time=[]
		lots_A=[]
		nameB=[]
		openB=[]
		openB_time=[]
		closeB=[]
		closeB_time=[]
		lots_B=[]
		order_type=[]
		orderid=[]
		ln_e_open=[]
		ln_e_close=[]
		sql=""
		shutil.copy("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order/"+filename,"C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order/test/"+filename)
		csvfile=open("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order/test/"+filename)
		reader = csv.reader(csvfile)
		for row in reader:
			nameA.append(row[0])
			openA.append(row[1])
			openA_time.append(row[2])
			closeA.append(row[3])
			closeA_time.append(row[4])
			lots_A.append(row[5])
			order_type.append(row[6])
			orderid.append(row[8])
			ln_e_open.append(row[9])
			ln_e_close.append(row[10])
		#决策函数
		
		for i in range(len(nameA)):
			writelog("平仓订单"+nameA[i]+","+order_type[i])
			sql=sql+"insert into stock_lmx.order_result values (null,'"+nameA[i]+"','"+openA[i]+"','"+openA_time[i]+"','"+closeA[i]+"','"+closeA_time[i]+"','"+lots_A[i]+"',null,'null','null','null','unll','null','"+order_type[i]+"','"+orderid[i]+"','"+ln_e_open[i]+"','"+ln_e_close[i]+"');"
		#print(sql)
		csvfile.close()
		time.sleep(3)
		os.remove("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order/"+filename)
		cur_stock.execute(sql)
def writelog(str):
	file=open("mail_result.ini","a")
	file.write(str+"\n")
	file.close()		


if __name__ == "__main__":

	while(3):
		if len(getFileList("C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/6A8058911C98E1D14B8F4592B28ED9C5/MQL4/Files/order"))>0:
			
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_lmx',port=3306)
			cur_stock=conn.cursor()
			cur_result=conn.cursor()
			cur_d=conn.cursor()
			cur_check=conn.cursor()
			cur_result_DB=conn.cursor()
			cur_stock_releation=conn.cursor()
			load_report()
			#mail.run("mail_result.ini","有平仓订单,请查看,具体内容暂时没打印")
			cur_check.close()
			cur_result.close()
			cur_d.close()
			cur_check.close()
			cur_stock_releation.close()
			conn.commit()
			conn.close()
	

