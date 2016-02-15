#coding:utf-8
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

def loadcsv ():#核心函数，查URL写数据库,计算指标库
	#sql="delete from stock_test;"
	sql=""
	s=os.getcwd()
	for filename in getFileList(os.getcwd()+"\stock-data"):
		print(filename)
		high=[]
		low=[]
		open_=[]
		close=[]
		amount=[]
		date_=[]
		time_=[]
		reader = csv.reader(open("stock-data/"+filename))
		for row in reader:
			date_.append(row[0])
			time_.append(row[1])
			open_.append(row[2])
			high.append(row[3])
			low.append(row[4])
			close.append(row[5])
			amount.append(row[6])
		for i in range(len(date_)):
			#sql=sql+"insert into stock_lmx.stock values ('"+filename[0:6]+"','"+date_[i]+"','"+time_[i]+"',null,null,null,'"+close[i]+"',null,0,null);"
			sql=sql+"insert into stock_lmx.stock_back values ('"+filename[0:10]+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"','"+high[i]+"','"+low[i]+"','"+close[i]+"',null,0,null);"

		cur_stock.execute(sql)
		sql=""
	
	
	
def pearson(x,y):
	stockid=[]
	time1=[]
	n=len(x)
	vals=range(n)
	# Simple sums
	sumx=sum([float(x[i]) for i in vals])
	sumy=sum([float(y[i]) for i in vals])
	# Sum up the squares

	sumxSq=sum([x[i]**2.0 for i in vals])
	sumySq=sum([y[i]**2.0 for i in vals])
	# Sum up the products
	pSum=sum([x[i]*y[i] for i in vals])
	# Calculate Pearson score
	num=pSum-(sumx*sumy/n)
	den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
	if den==0: return 0
	r=num/den
	return r



def st_norm(u):
	x=abs(u)/math.sqrt(2)
	T=(0.0705230784,0.0422820123,0.0092705272,0.0001520143,0.0002765672,0.0000430638)
	E=1-pow((1+sum([a*pow(x,(i+1)) for i,a in enumerate(T)])),-16)
	p=0.5-0.5*E if u<0 else 0.5+0.5*E
	return(p)
  
def norm(x,a,sigma):

	u=(x-a)/sigma
	return(st_norm(u))

def stdev(self):
	if len(self) < 1:
		return None
	else:
		avg = sum(self)/len(self)
		sdsq = sum([(i - avg) ** 2 for i in self])
		stdev = (sdsq / (len(self) - 1)) ** .5
		return stdev

def releation_mid(sample,tablename):#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	a=[]
	b=[]
	#sql="SELECT stockid FROM stock_lmx.stock GROUP BY stockid;"
	sql="SELECT stockid FROM stock_lmx.stock_back  GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	print(str(tablename)+"函数内取出的值",len(res))
	if len(res)>1:
		dict1={}
		sql="DELETE FROM stock_back WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')<DATE_ADD(NOW(),INTERVAL -5 DAY);"
		cur_result.execute(sql)
		
if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_lmx',port=3306)
	cur_stock=conn.cursor()
	loadcsv()
	cur_stock.close()
	conn.commit()
	conn.close()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_lmx',port=3306)
	cur_stock=conn.cursor()
	cur_result=conn.cursor()
	#releation_mid(100,"releation_mid")
	conn.commit()
	cur_stock.close()
	cur_result.close()
	conn.close()
