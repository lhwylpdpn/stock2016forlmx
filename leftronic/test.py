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
	#sql="SELECT stockid FROM stock_foreign.stock GROUP BY stockid;"
	sql="SELECT stockid FROM stock_foreign.stock GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	print(str(tablename)+"函数内取出的值",len(res))
	if len(res)>1:
		dict1={}
		sql="delete from "+str(tablename)+";"
		cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
			for j in range(len(stockid)):
				if i<j:

					
					sql="select DISTINCT a.date,a.time,a.close,b.close from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') desc LIMIT "+str(sample+2)
					cur_stock.execute(sql)
					res=cur_stock.fetchall()
					for r in res:
						try:
							#print(str(r[1]))
							lnA_B.append(math.log(float(r[2])) - math.log(float(r[3])))
							close_1.append(float(r[2]))
							close_2.append(float(r[3]))
							date1.append(str(r[0]))
							time1.append(str(r[1]))
							#print(float(r[2]),float(r[3]),str(r[0]),str(r[1]))
							#print(math.log(float(r[2])))
							#print(math.log(float(r[3])))
						except Exception as e:
							print(str(r[1]),str(r[0]),"C端读入数据有问题")
					if len(close_1)>=sample:
					#print(pearson(close_1,close_2),close_1,close_2)
						#print(lnA_B[0],close_1[0])
						sql="insert into "+str(tablename)+" values('"+stockid[i]+"','"+stockid[j]+"','"+str(sample)+"','"+str(pearson(close_1[0:sample],close_2[0:sample]))+"','"+str(lnA_B[0])+"','"+str(sum(lnA_B[0:sample])/len(lnA_B[0:sample]))+"','"+str(stdev(lnA_B[0:sample]))+"','"+str(scipy.stats.norm.cdf(lnA_B[0],sum(lnA_B[1:sample+1])/len(lnA_B[1:sample+1]),stdev(lnA_B[1:sample+1])))+"','"+str(scipy.stats.norm.cdf(lnA_B[1],sum(lnA_B[2:sample+2])/len(lnA_B[2:sample+2]),stdev(lnA_B[2:sample+2])))+"');"
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

def decision(name,close,norm_list,commission):
	stockA=[]
	stockB=[]
	releation=[]
	lnA_B=[]
	avgA_B=[]
	stdA_B=[]
	lnA_B_now=[]
	normA_B_now=[]
	orderid=[]
	lnA_B_except=[]
	n=len(name)
	n2=len(close)
	if n!=n2:
		print("文件读入的数据中结构不正确,name和close不匹配")
	else:

		sql="SELECT a.stockidA, a.stockidB ,a.releation ,a.lnA_B,a.avgA_B,a.stdA_B,b.`releation` FROM releation_mid a, releation_mid_prev b WHERE a.`stockidA`=b.`stockidA` AND a.`stockidB`=b.`stockidB`  and a.norm_ln_prev<0.9 and a.norm_ln_prev>0.1   AND a.norm_ln_prev2<0.9 AND a.norm_ln_prev2>0.1 "
		cur_d.execute(sql)
		res=cur_d.fetchall()
		print("decision",len(res))
		if len(res)>0:
			for r in res:
				
				if float(r[6])>0.9 and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])+commission),float(r[4]),float(r[5]))>norm_list and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))<0.99:# and abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])) - scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))>0.5:#获取每一组A和B在参数的位置，并找出位置的close为现价，做计算后合并为lnA_B_now
					print(abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))-scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5]))))
					print(float(r[3]))
					print(scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))
					print(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])))
					stockA.append(str(r[0]))
					stockB.append(str(r[1]))
					releation.append(float(r[2]))
					lnA_B.append(float(r[3]))
					avgA_B.append(float(r[4]))
					stdA_B.append(float(r[5]))
					lnA_B_now.append(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])))
					normA_B_now.append(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])+commission),float(r[4]),float(r[5])))
					lnA_B_except.append(scipy.stats.norm.ppf(norm_list,float(r[4]),float(r[5])))
					orderid.append("0.9_0.99_"+str(time.time()+random.random()))
				if float(r[6])>0.9 and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])-commission),float(r[4]),float(r[5]))<(1-norm_list) and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))>0.01:# and abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])) - scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))>0.5:#获取每一组A和B在参数的位置，并找出位置的close为现价，做计算后合并为lnA_B_now
					print(abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))-scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5]))))
					print(float(r[3]))
					print(scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))
					print(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])))
					stockA.append(str(r[1]))
					stockB.append(str(r[0]))
					releation.append(float(r[2]))
					lnA_B.append(float(r[3]))
					avgA_B.append(float(r[4]))
					stdA_B.append(float(r[5]))
					lnA_B_now.append(-math.log(float(close[name.index(str(r[0]))]))+math.log(float(close[name.index(str(r[1]))])))
					normA_B_now.append(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])-commission),float(r[4]),float(r[5])))
					lnA_B_except.append(-scipy.stats.norm.ppf((1-norm_list),float(r[4]),float(r[5])))
					orderid.append("0.9_0.01_"+str(time.time()+random.random()))
			#print(normA_B_now)
		#如果releation>0.9 且 norm>0.99 就可以满足下单
			if len(stockA)>0:
				write_API(stockB,stockA,lnA_B_now,lnA_B_except,orderid)
				result_DB(stockB,stockA,lnA_B_now,lnA_B_except,normA_B_now,releation,orderid,avgA_B,stdA_B)

def report_1():
	sql="SELECT a,b,c,d,(a*c+b*d) AS e FROM (SELECT COUNT(CASE WHEN order_type=1 THEN 1 END )/COUNT(*) * SUM(CASE WHEN order_type=1 THEN ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B) END)/COUNT(*) AS a , COUNT(CASE WHEN order_type=0 THEN 1 END )/COUNT(*) * SUM(CASE WHEN order_type=1 THEN ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B) END)/COUNT(*) AS b,COUNT(CASE WHEN order_type=1 THEN 1 END )/COUNT(*)  AS c,COUNT(CASE WHEN order_type=0 THEN 1 END )/COUNT(*)  AS d FROM `order_result`) a "
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	if len(res)>0:
		for r in res:
			os.system("report_1.bat "+str(r[0])+" "+str(r[1])+" "+str(r[2])+" "+str(r[3])+" "+str(r[4]))
if __name__ == '__main__':
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()
	report_1()
	cur_stock.close()
	conn.close()
