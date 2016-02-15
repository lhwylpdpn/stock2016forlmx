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


# def run():#主循环运算函数
# 	sql="select distnict stockidA,stockidB from  model_data_model;"
# 	cur_stock.execute(sql)
# 	res=cur_stock.fetchall()
# 	res_all=len(res)
# 	if len(res)>0:
# 		for r in res:
# 			sql="select stockidA,stockidB,releation,ln,lnA_B-C,lnA_B+C,C,norm,norm_num,date,time from model_data_model where stockidA='"+r[0]+"' and stockidB='"+r[1]+"' ORDER BY  STR_TO_DATE(CONCAT(date,' ',TIME),'%Y.%c.%d %H:%i')"
# 			cur_stock.execute(sql)
# 			res=cur_stock.fetchall()
# 			for i in res:
# 				if decision_open(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10])==1:
# 					open_.append(1)
# 				else:
# 					open.append("")
# 			close()
def run(stockid_i,stockid_j,date1,time1,lnA_B,lnA_B_sub,lnA_BsubC,lnA_BaddC,close_1,close_2,norm_,pearson_,avg_,stdev_,sample,commission,norm_num):
	print(stockid_i[1],stockid_j[1])
	open_=[]
	close_=[]
	clsoe_stats=[]
	values=[]
	zhengtai_count=0
	zhisun_count=0
	zhengtai_time=[]
	zhisun_time=[]
	zhengtai_value=[]
	zhisun_value=[]

	for i in range(len(lnA_B)):
		#if i>700 and i<750:

			#print(i,pearson_[i],pearson_[i-1],scipy.stats.norm.cdf(lnA_BaddC[i],avg_[i],stdev_[i]))
		if i>101 and pearson_[i-1]>0.9 and scipy.stats.norm.cdf(math.log(close_1[i]-commission)-math.log(close_2[i]+commission)-lnA_B[i-1],avg_[i],stdev_[i])>0.9: #and abs(scipy.stats.norm.cdf(lnA_BaddC[i-1],avg_[i],stdev_[i])-scipy.stats.norm.cdf(lnA_BaddC[i],avg_[i],stdev_[i]))>0.5:
			open_.append(1)
			
			for j in range(i+1,len(lnA_B)):
				if (close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i])< -0.005:
					close_.append(j)
					clsoe_stats.append("止损订单")
					values.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					zhisun_value.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					zhisun_count=zhisun_count+1
					zhisun_time.append(j-i)
					break
				if lnA_B[j]<scipy.stats.norm.ppf(0.9,avg_[i],stdev_[i])+lnA_B[i-1]:
					#print(lnA_B[j],scipy.stats.norm.ppf(0.9,avg_[i],stdev_[i]),lnA_B_sub[i-1])
					close_.append(j)
					clsoe_stats.append("正态交易")
					values.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					zhengtai_value.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					zhengtai_count=zhengtai_count+1
					zhengtai_time.append(j-i)
					break
				if j==len(lnA_B)-1:
					close_.append(0)
					clsoe_stats.append(0)		
					values.append(0)	
				
		elif i>101 and pearson_[i-1]>0.9 and scipy.stats.norm.cdf(math.log(close_1[i]+commission)-math.log(close_2[i]-commission)-lnA_B[i-1],avg_[i],stdev_[i])<0.1 : #and abs(scipy.stats.norm.cdf(lnA_BaddC[i-1],avg_[i],stdev_[i])-scipy.stats.norm.cdf(lnA_BaddC[i],avg_[i],stdev_[i]))>0.5:
			open_.append(1)
			for j in range(i+1,len(lnA_B)):
				if (close_1[j]-close_1[i]+close_2[i]-close_2[j])/(close_1[i]+close_2[i])<-0.005:
					close_.append(j)
					clsoe_stats.append("止损订单")
					values.append((close_1[j]-close_1[i]+close_2[i]-close_2[j])/(close_1[i]+close_2[i]))
					zhisun_value.append((close_1[j]-close_1[i]+close_2[i]-close_2[j])/(close_1[i]+close_2[i]))
					zhisun_count=zhisun_count+1
					zhisun_time.append(j-i)
					break
				if lnA_B[j]>scipy.stats.norm.ppf(0.1,avg_[i],stdev_[i])+lnA_B[i-1]:
					close_.append(j)
					clsoe_stats.append("正态交易")
					values.append((close_1[j]-close_1[i]+close_2[i]-close_2[j])/(close_1[i]+close_2[i]))
					zhengtai_value.append((close_1[j]-close_1[i]+close_2[i]-close_2[j])/(close_1[i]+close_2[i]))
					zhengtai_count=zhengtai_count+1
					zhengtai_time.append(j-i)
					break
				if j==len(lnA_B)-1:
					close_.append(0)
					clsoe_stats.append(0)		
					values.append(0)		
				
		else:
			open_.append(0)
			close_.append(0)
			clsoe_stats.append(0)		
			values.append(0)

	if zhengtai_count!=0 or zhisun_count!=0:
		chenggonglv=str(zhengtai_count/(zhengtai_count+zhisun_count))
	else:
		chenggonglv=0
	if len(zhengtai_time)!=0:
		zhengtai_time1=sum(zhengtai_time)/len(zhengtai_time)
	else:
		zhengtai_time1=0
	if len(zhisun_time)!=0:
		zhisun_time1=sum(zhisun_time)/len(zhisun_time)
	else:
		zhisun_time1=0
	if len(zhisun_value)!=0:
		zhisun_value1=sum(zhisun_value)/len(zhisun_value)
	else:
		zhisun_value1=0
	if len(zhengtai_value)!=0:
		zhengtai_value1=sum(zhengtai_value)/len(zhengtai_value)
	else:
		zhengtai_value1=0
	#writle_connt(stockid_i[0]+","+stockid_j[0]+","+str(zhengtai_count)+","+str(zhisun_count)+","+str(chenggonglv)+","+str(sum([abs(r-sum(lnA_B)/len(lnA_B)) for r in lnA_B])/len(lnA_B))+","+str(zhengtai_time1)+","+str(zhisun_time1)+","+str(zhengtai_value1)+","+str(zhisun_value1))
	#print(stockid_i,stockid_j)

	write_result(stockid_i,stockid_j,date1,time1,lnA_B,lnA_B_sub,lnA_BsubC,lnA_BaddC,close_1,close_2,norm_,pearson_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values)

def write_result(stockid_i,stockid_j,date1,time1,lnA_B,lnA_B_sub,lnA_BsubC,lnA_BaddC,close_1,close_2,norm_,pearson_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values):
	file_object = open('result.csv','w')

	file_object.write("id,stockid_i,stockid_j,date1,time1,lnA_B,lnA_B_sub,lnA_BsubC,lnA_BaddC,close_1,close_2,pearson_,norm_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values"+"\n")
	# print(len(stockid_i))
	# print(len(stockid_j))
	# print(len(date1))
	# print(len(time1))
	# print(len(lnA_B))
	# print(len(lnA_BsubC))
	# print(len(lnA_BaddC))
	# print(len(close_1))
	# print(len(close_2))
	# print(len(norm_))
	# print(len(pearson_))
	# print(len(avg_))
	# print(len(stdev_))

	# print(len(open_))
	# print(len(close_))
	# print(len(clsoe_stats))
	# print(len(values))

	for i in range(len(lnA_B)):
		file_object.write(str(i)+","+str(stockid_i[i])+","+str(stockid_j[i])+","+str(date1[i])+","+str(time1[i])+","+str(lnA_B[i])+","+str(lnA_B_sub[i])+","+str(lnA_BsubC[i])+","+str(lnA_BaddC[i])+","+str(close_1[i])+","+str(close_2[i])+","+str(pearson_[i])+","+str(norm_[i])+","+str(avg_[i])+","+str(stdev_[i])+","+str(sample)+","+str(commission)+","+str(norm_num)+","+str(open_[i])+","+str(close_[i])+","+str(clsoe_stats[i])+","+str(values[i])+"\n")
	file_object.close()

def data_clear(sample,commission,norm_num):#补充指标函数
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	a=[]
	b=[]
	lnA_BsubC=[]
	lnA_BaddC=[]
	pearson_=[]
	norm_=[]
	stockid_j=[]
	stockid_i=[]
	lnA_B_sub=[]
	avg_=[]
	stdev_=[]
	res_all=0
	res_now=0
	sql="SELECT stockid FROM stock_foreign.stock  where stockid in ('GBPCAD','GBPSGD') GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	#print(len(res))

	res_all=len(res)

	if len(res)>1:
		dict1={}
		sql=""
		# sql="delete from model_data_model;"
		# cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
			for j in range(len(stockid)):
				if i<j:
					print(0)
					sql2="select DISTINCT a.date,a.time,a.close,b.close from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') "
					cur_stock.execute(sql2)
					res=cur_stock.fetchall()
					print(1)
					for r in res:
						try:
							stockid_i.append(stockid[i])
							stockid_j.append(stockid[j])
							lnA_BsubC.append(math.log(float(r[2])) - math.log(float(r[3]-commission)))
							lnA_BaddC.append(math.log(float(r[2])) - math.log(float(r[3]+commission)))
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
					
					#time.sleep(5)
					for r in range(0,len(close_1)):
						if r>0:
							lnA_B_sub.append(lnA_B[r]-lnA_B[r-1])
							#print(lnA_B[r],lnA_B[r-1],lnA_B_sub[r])
						else:
							lnA_B_sub.append(0)
						if r>=sample:
							
							norm_.append(scipy.stats.norm.cdf(lnA_B_sub[r],sum(lnA_B_sub[r-sample:r])/sample,stdev(lnA_B_sub[r-sample:r])))
							avg_.append(sum(lnA_B_sub[r-sample:r])/sample)
							stdev_.append(stdev(lnA_B_sub[r-sample:r]))
							pearson_.append(pearson(close_1[r-sample:r],close_2[r-sample:r]))

						else:
							pearson_.append("")
							norm_.append("")
							avg_.append("")
							stdev_.append("")

					print(3)
					if len(close_1)>=sample:
					
						run(stockid_i,stockid_j,date1,time1,lnA_B,lnA_B_sub,lnA_BsubC,lnA_BaddC,close_1,close_2,norm_,pearson_,avg_,stdev_,sample,commission,norm_num)

							#sql=sql+"insert into  model_data_model values('"+stockid[i]+"','"+stockid[j]+"','"+str(sample)+"','"+str(pearson_[r])+"','"+str(lnA_B[r])+"','"+str(lnA_BsubC[r])+"','"+str(lnA_BaddC[r])+"','"+str(commission)+"','"+str(norm_[r])+"','"+str(norm_num)+"','"+str(date1[r])+"','"+str(time1[r])+"');"
					else:
						print(stockid[i],stockid[j],"并不够"+str(sample)+"条记录")
					# print(str(pearson(close_1,close_2)))
					# print(str(pearson(per_1,per_2)))
					# print(str(pearson(close_1[0:30],close_2[0:30])))
					# print(str(pearson(per_1[0:30],per_2[0:30])))
					# print(str(pearson(close_1[0:500],close_2[0:500])))
					# print(str(pearson(per_1[0:500],per_2[0:500])))
					# print(len(res))
					print(4)
					close_1=[]
					close_2=[]
					date1=[]
					time1=[]
					lnA_B=[]
					a=[]
					b=[]
					avg_=[]
					stdev_=[]
					lnA_BsubC=[]
					lnA_BaddC=[]
					pearson_=[]
					norm_=[]
					stockid_j=[]
					stockid_i=[]
					lnA_B_sub=[]
					res_now=res_now+1
					#print(str(round(res_now)))


def writelog(str):
	file=open("mail.ini","a")
	file.write(str+"\n")
	file.close()

########################################数学相关函数	####################################################################
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
######################################################################################################										
if __name__ == "__main__":
	# write_API("GBPUSD","USDCHF",-0.24836,-0.401,"33133333333333")
	# conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# cur_stock=conn.cursor()
	# cur_action=conn.cursor()
	# cur_result=conn.cursor()
	# cur_d=conn.cursor()
	# cur_check=conn.cursor()
	# cur_result_DB=conn.cursor()
	# cur_stock_releation=conn.cursor()
	# releation_mid(100)
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()
	cur_result=conn.cursor()
	cur_d=conn.cursor()
	cur_check=conn.cursor()
	cur_result_DB=conn.cursor()
	cur_stock_releation=conn.cursor()

	data_clear(100,0.0006,0.9)








	cur_result.close()
	cur_d.close()
	cur_check.close()
	cur_stock_releation.close()
	conn.commit()
	conn.close()




	#print(scipy.stats.norm.ppf(0.99,0.00468906,0.49432524))

	# while(1):

	# 	if  (os.path.getsize("C:/Users/Administrator/AppData/Roaming/MeaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/API_callback.csv")!=0):
	# 		conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# 		cur_stock=conn.cursor()
	# 		cur_action=conn.cursor()
	# 		cur_result=conn.cursor()
	# 		print("有新增数据入库"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			
	
	# 		cur_stock.execute("delete from releation")
	# 		loadcsv_add()
	# 		calc1()
	# 		cur_result.execute("delete from norm_data")
	# 		stockid=[]
	# 		sql233="SELECT stockidA,stockidB FROM `releation` WHERE   relation_per_1000>0.93 LIMIT 10"
	# 		cur_result.execute(sql233)
	# 		res=cur_result.fetchall()
	# 		for j in res:
	# 			calc(j[0],j[1])
	# 		sign(0.99,0.01,0.15)
	# 		print("计算完成step1"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	# 		sign_no_limit(0.99,0.01)
	# 		print("计算完成step2"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	# 		cur_result.close()
	# 		cur_action.close()
	# 		cur_stock.close()
	# 		conn.close()
	# 		time.sleep(60)
	# 		loadcsv_add_clear()

