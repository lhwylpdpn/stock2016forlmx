#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
import math
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
	for filename in getFileList(os.getcwd()+"\static-data"):
		print(filename)
		high=[]
		low=[]
		open_=[]
		close=[]
		amount=[]
		date_=[]
		time_=[]
		reader = csv.reader(open("static-data/"+filename))
		for row in reader:
			date_.append(row[0])
			time_.append(row[1])
			open_.append(row[2])
			high.append(row[3])
			low.append(row[4])
			close.append(row[5])
			amount.append(row[6])
		for i in range(len(date_)):
			sql=sql+"insert into stock_back values ('"+filename+"','"+date_[i]+"','"+time_[i]+"',null,null,null,'"+close[i]+"',null,null,null);"
		cur_stock.execute(sql)
		sql=""
	conn.commit()
	cur_stock.close()
	conn.close()
	
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

def releation_mid(sample):#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	a=[]
	b=[]
	sql="SELECT stockid FROM stock_foreign.stock GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	print("releation_mid函数内取出的值",len(res))
	if len(res)>1:
		dict1={}
		sql="delete from releation_mid;"
		cur_result.execute(sql)
		sql="DELETE FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')<DATE_ADD(NOW(),INTERVAL -5 DAY);"
		cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
			for j in range(len(stockid)):
				if i<j:

					sql="select DISTINCT a.date,a.time,a.close,b.close from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') desc LIMIT "+str(sample)
					cur_stock.execute(sql)
					res=cur_stock.fetchall()
					print(len(res))
					for r in res:

							#print(str(r[1]))
						lnA_B.append(math.log(float(r[2])) - math.log(float(r[3])))
						close_1.append(float(r[2]))
						close_2.append(float(r[3]))
						date1.append(str(r[0]))
						time1.append(str(r[1]))
							#print(float(r[2]),float(r[3]),str(r[0]),str(r[1]))
							#print(math.log(float(r[2])))
							#print(math.log(float(r[3])))

							#print(str(r[1]),str(r[0]),"C端读入数据有问题")
					if len(close_1)>=sample:
					#print(pearson(close_1,close_2),close_1,close_2)
					#print(close_1[len(close_1)-1],close_2[len(close_2)-1])
						sql="insert into releation_mid values('"+stockid[i]+"','"+stockid[j]+"','"+str(sample)+"','"+str(pearson(close_1,close_2))+"','"+str(lnA_B[len(lnA_B)-1])+"','"+str(sum(lnA_B)/len(lnA_B))+"','"+str(stdev(lnA_B))+"');"
						cur_result.execute(sql)
					else:
						print(stockid[i],stockid[j],"并不够"+str(sample)+"条记录")
					# print(str(pearson(close_1,close_2)))
					# print(str(pearson(per_1,per_2)))
					# print(str(pearson(close_1[0:30],close_2[0:30])))
					# print(str(pearson(per_1[0:30],per_2[0:30])))
					# print(str(pearson(close_1[0:500],close_2[0:500])))
					# print(str(pearson(per_1[0:500],per_2[0:500])))
					# print(len(res))

					close_1=[]
					close_2=[]
					lnA_B=[]
					date1=[]
					time1=[]


if __name__ == "__main__":
	time1=time.time()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()

	loadcsv()
	cur_stock.close()
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()
	cur_result=conn.cursor()

	conn.commit()
	cur_stock.close()
	cur_result.close()
	conn.close()
