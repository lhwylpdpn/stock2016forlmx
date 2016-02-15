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



def	run1(stockid_i,date1,time1,lnA_B,lnA_B_sub,close_1,norm_,avg_,stdev_,sample,commission,norm_num,norm_lncha,norm_temp):

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
	huiche=[]
	qushi_open_=[]
	qushi_close_=[]
	qushi_value=[]
	qushi_zhiying_count=0
	qushi_zhiying_value=[]
	qushi_zhiying_time=[]
	qushi_huiche=[]
	qushi_zhisun_value=[]
	qushi_zhisun_count=0
	qushi_zhisun_time=[]
	qushi_clsoe_stats=[]
	cangweiall=0
	cangwei=[]
	zd_zhiying_value=[]
	zd_open=[]
	zd_count=[]
	zd_close_status=[]
	zd_count_max=[]

	zd_zhisun_value=[]
	zd_c_max_count_max=[]
	zd_c_max_count=[]
	zd_c_max_zhiying_value=[]
	zd_c_max_chicang=[]
	zd_c_avg_chicang=[]

	chicang=[]
	for i in range(len(lnA_B)):#所有日期的价格
		zd_open.append(0)
		zd_count.append(0)
		zd_open.append(close_1[i]) #开仓价list
		zd_count.append(1)
		chicang.append(1)
		zd_count_max.append(0)
		for j in range(i+1,len(lnA_B)): #一次日期的价格在后续所有天数里
			#print(close_1[j],zd_open[len(zd_open)-1])
			if close_1[j]-zd_open[len(zd_open)-1]>close_1[i]*0.01:

				zd_zhiying_value.append((close_1[j]-zd_open[len(zd_open)-1])*zd_count[len(zd_count)-1])
				zd_open.pop()
				zd_count.pop()
				

				#zd_close_status.append(str(j)+","+str(zd_open(len(qushi_open))))
			#print(len(zd_count),zd_count[len(zd_count)-1])
			if len(zd_count)==1:
				chicang.append(j-i)
				break
				
			if close_1[j]-zd_open[len(zd_open)-1]<-close_1[i]*0.01:
				zd_zhisun_value.append((close_1[j]-zd_open[len(zd_open)-1])*zd_count[len(zd_count)-1])
				zd_open.append(close_1[j])

				zd_count.append(zd_count[len(zd_count)-1]+zd_count[len(zd_count)-2])
				
				zd_count_max.append((zd_count[len(zd_count)-1]+zd_count[len(zd_count)-2]))
		#print(zd_open[len(zd_open)-1],zd_count[len(zd_count)-1],sum(zd_zhiying_value),max(zd_count_max),chicang)
		zd_c_max_count_max.append(max(zd_count_max))
		zd_c_max_count.append(zd_count[len(zd_count)-1])
		zd_c_max_zhiying_value.append(sum(zd_zhiying_value))
		zd_c_max_chicang.append(max(chicang))
		zd_c_avg_chicang.append(sum(chicang)/len(chicang))
		#zd_c_max_count_max.append()
		zd_open=[]
		zd_count=[]
		zd_zhiying_value=[]
		chicang=[]
		zd_zhisun_value=[]
		zd_c_chengbenall=[]
		#writle_test(str(stockid_i[i])+","+str(date1[i])+","+str(time1[i])+","+str(close_1[i])+","+str(max(zd_count))+","+str(max(zd_zhiying_value))+","+str(max(zd_c_avg_chicang)))

	writle_test(str(stockid_i[i])+","+str(max(zd_c_max_count_max))+","+str(max(zd_c_max_count))+","+str(zd_c_max_count[len(zd_c_max_count)-1])+","+str(max(zd_c_max_zhiying_value))+","+str(max(zd_c_max_chicang))+","+str(max(zd_c_avg_chicang))+","+str(sum(close_1)/len(close_1)))

def writle_test(word):
	#print(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	file_object = open('count323.csv','a')
	file_object.write(word+"\n")
	file_object.close()
def wrilte_title_one():
	file_object = open('count323.csv','a')
	file_object.write("name,同时持有最大,补仓最多次数,最大剩余仓位,总盈利,最大持仓时间,最大平均持仓时间"+"\n")
	file_object.close()

def writle_test_one(word):
	#print(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	file_object = open('result.csv','w')
	file_object.write(word+"\n")
	file_object.close()










def	run(stockid_i,date1,time1,lnA_B,lnA_B_sub,close_1,norm_,avg_,stdev_,sample,commission,norm_num,norm_lncha,norm_temp):

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
	huiche=[]
	qushi_open_=[]
	qushi_close_=[]
	qushi_value=[]
	qushi_zhiying_count=0
	qushi_zhiying_value=[]
	qushi_zhiying_time=[]
	qushi_huiche=[]
	qushi_zhisun_value=[]
	qushi_zhisun_count=0
	qushi_zhisun_time=[]
	qushi_clsoe_stats=[]
	cangweiall=0
	cangwei=[]
	zd_zhiying_value=[]
	zd_open=[]
	zd_count=[]
	zd_close_status=[]
	zd_count_max=[]

	zd_zhisun_value=[]
	zd_c_max_count_max=[]
	zd_c_max_count=[]
	zd_c_max_zhiying_value=[]
	zd_c_max_chicang=[]
	zd_c_avg_chicang=[]

	chicang=[]
	# for i in range(len(lnA_B)):
		#print(2,len(lnA_B),len(values),len(clsoe_stats),len(open_))
		#time.sleep(1)
		#if i>700 and i<750:
		# if i>=len(lnA_B)-1 or norm_temp[i]=="" or norm_temp[i-1]=="" or norm_temp[i-2]==""  or norm_temp[i-3]=="" :
		# 	qushi_open_.append(0)
		# 	qushi_close_.append(0)
		# 	qushi_clsoe_stats.append(0)		
		# 	qushi_value.append(0)
		# 	qushi_huiche.append(0)
		# 	continue

		# #print(norm_lncha[i],1,norm_temp[i],2,norm_temp[i-1],3,norm_temp[i-2],4,norm_temp[i-3])
		# if i>103  and  norm_lncha[i]>0.999 or (norm_temp[i]>0.9 and norm_temp[i-1]>0.9 and norm_temp[i-2]>0.9  and norm_temp[i-3]>0.9):
		# 	qushi_open_.append(1)
		# 	#print(i+1,len(lnA_B))
		# 	for j in range(i+1,len(lnA_B)):

		# 		if (close_1[j]-close_1[i])/close_1[i]>0.002:
					
		# 			qushi_close_.append(j)
		# 			qushi_clsoe_stats.append("追涨成功")
		# 			qushi_value.append((close_1[j]-close_1[i])/close_1[i])
		# 			qushi_zhiying_value.append((close_1[j]-close_1[i])/close_1[i])
		# 			qushi_zhiying_count=qushi_zhiying_count+1
		# 			qushi_zhiying_time.append(j-i)
		# 			qushi_huiche.append(0)

		# 			break				
		# 		if (close_1[j]-close_1[i])/close_1[i]<-0.002:
					
		# 			qushi_close_.append(j)
		# 			qushi_clsoe_stats.append("追涨失败")
		# 			qushi_value.append((close_1[j]-close_1[i])/close_1[i])
		# 			qushi_zhisun_value.append((close_1[j]-close_1[i])/close_1[i])
		# 			qushi_zhisun_count=qushi_zhisun_count+1
		# 			qushi_zhisun_time.append(j-i)
		# 			qushi_huiche.append(0)
		# 			break	
		# 		if j>=len(lnA_B)-1:
		# 			#print(3,len(open_),len(close_))
		# 			qushi_close_.append(-1)
		# 			qushi_clsoe_stats.append(-1)		
		# 			qushi_value.append(-1)
		# 			qushi_huiche.append(0)	

	# 	elif i>103 and  i<len(lnA_B)-2 and norm_lncha[i]<0.001 or (norm_temp[i]<0.1 and norm_temp[i-1]<0.1  and norm_temp[i-2]<0.1  and norm_temp[i-3]<0.1 ):
	# 		qushi_open_.append(1)
	# 		for j in range(i+1,len(lnA_B)):

	# 			if (close_1[i]-close_1[j])/close_1[i]>0.002:
					
	# 				qushi_close_.append(j)
	# 				qushi_clsoe_stats.append("追涨成功")
	# 				qushi_value.append((close_1[i]-close_1[j])/close_1[i])
	# 				qushi_zhiying_value.append((close_1[i]-close_1[j])/close_1[i])
	# 				qushi_zhiying_count=qushi_zhiying_count+1
	# 				qushi_zhiying_time.append(j-i)
	# 				qushi_huiche.append(0)

	# 				break				
	# 			if (close_1[i]-close_1[j])/close_1[i]<-0.002:
					
	# 				qushi_close_.append(j)
	# 				qushi_clsoe_stats.append("追涨失败")
	# 				qushi_value.append((close_1[i]-close_1[j])/close_1[i])
	# 				qushi_zhisun_value.append((close_1[i]-close_1[j])/close_1[i])
	# 				qushi_zhisun_count=qushi_zhisun_count+1
	# 				qushi_zhisun_time.append(j-i)
	# 				qushi_huiche.append(0)
	# 				break		
	# 			if j>=len(lnA_B)-1:
	# 				#print(3,len(open_),len(close_))
	# 				qushi_close_.append(-1)
	# 				qushi_clsoe_stats.append(-1)		
	# 				qushi_value.append(-1)
	# 				qushi_huiche.append(0)					
	# 	else:
	# 		qushi_open_.append(0)
	# 		qushi_close_.append(0)
	# 		qushi_clsoe_stats.append(0)
	# 		qushi_value.append(0)
	# 		qushi_huiche.append(0)			

	# if qushi_zhiying_count!=0 or qushi_zhisun_count!=0:
	# 	qushi_chenggonglv=str(qushi_zhiying_count/(qushi_zhiying_count+qushi_zhisun_count))
	# else:
	# 	qushi_chenggonglv=0
	# if len(qushi_zhiying_time)!=0:
	# 	qushi_zhiying_time1=sum(qushi_zhiying_time)/len(qushi_zhiying_time)
	# else:
	# 	qushi_zhiying_time1=0
	# if len(qushi_zhisun_time)!=0:
	# 	qushi_zhisun_time1=sum(qushi_zhisun_time)/len(qushi_zhisun_time)
	# else:
	# 	qushi_zhisun_time1=0
	# if len(qushi_zhisun_value)!=0:
	# 	qushi_zhisun_value1=sum(qushi_zhisun_value)/len(qushi_zhisun_value)
	# else:
	# 	qushi_zhisun_value1=0
	# if len(qushi_zhiying_value)!=0:
	# 	qushi_zhiying_value1=sum(qushi_zhiying_value)/len(qushi_zhiying_value)
	# else:
	# 	qushi_zhiying_value1=0

##################################################################################################################################################

#↑↑↑↑↑↑↑↑追高策略↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

############################################################################################################################################

	for i in range(len(lnA_B)):



		if norm_[i]=="" or norm_[i-1]=="" or norm_[i-2]=="":
			open_.append(0)
			close_.append(0)
			clsoe_stats.append(0)		
			values.append(0)
			huiche.append(0)
			continue







		if i>102 and norm_[i]>0.9 and  norm_[i]<0.99 and norm_lncha[i]<0.9 and norm_[i-1]<0.9 and norm_[i-2]<0.9:#and norm_[i]-min(norm_[i-1],norm_[i-2],norm_[i-3])<0.6:
			if i+1<len(lnA_B):
				open_.append(1)
				
				for j in range(i+1,len(lnA_B)):
					
					if lnA_B[j]+0.001<scipy.stats.norm.ppf(0.85,avg_[i],stdev_[i]):
						#print(lnA_B[j],scipy.stats.norm.ppf(0.9,avg_[i],stdev_[i]),lnA_B_sub[i-1])
						
						close_.append(j)
						clsoe_stats.append("正态交易")
						values.append((close_1[i]-close_1[j])/close_1[i])
						zhengtai_value.append((close_1[i]-close_1[j])/close_1[i])
						zhengtai_count=zhengtai_count+1
						zhengtai_time.append(j-i)
						huiche.append((close_1[i]-max(close_1[i:j]))/close_1[i])
						#print(close_1[i],max(close_1[i:j]))
						break
					if (close_1[i]-close_1[j])/close_1[i]< -0.005:
						
						close_.append(j)
						clsoe_stats.append("止损订单")
						values.append((close_1[i]-close_1[j])/close_1[i])
						zhisun_value.append((close_1[i]-close_1[j])/close_1[i])
						zhisun_count=zhisun_count+1
						zhisun_time.append(j-i)
						huiche.append(0)

						break
				#for j in range(i+1,len(lnA_B)):
					# if (close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i])> 0.005:
					# 	close_.append(j)
					# 	clsoe_stats.append("止赢订单")
					# 	values.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					# 	zhengtai_value.append((close_1[i]-close_1[j]+close_2[j]-close_2[i])/(close_1[i]+close_2[i]))
					# 	zhengtai_count=zhisun_count+1
					# 	zhengtai_time.append(j-i)
					# 	break
					
			
			
					if j>=len(lnA_B)-1:
						#print(3,len(open_),len(close_))
						close_.append(-1)
						clsoe_stats.append(-1)		
						values.append(-1)
						huiche.append(0)	
			else:
				open_.append(0)
				close_.append(0)
				clsoe_stats.append(0)		
				values.append(0)
				huiche.append(0)
				
		elif i>102  and norm_[i]<0.12 and norm_[i]>0.01 and  norm_[i]>0.01 and norm_lncha[i]>0.1 and norm_[i-1]>0.1 and norm_[i-2]>0.1:#  and norm_[i]-max(norm_[i-1],norm_[i-2],norm_[i-3])>-0.6: #and abs(scipy.stats.norm.cdf(lnA_BaddC[i-1],avg_[i],stdev_[i])-scipy.stats.norm.cdf(lnA_BaddC[i],avg_[i],stdev_[i]))>0.5:
			#print(2,len(open_),len(close_))
			if i+1<len(lnA_B):
				open_.append(1)
				
				for j in range(i+1,len(lnA_B)):
					
					if lnA_B[j]-0.001>scipy.stats.norm.ppf(0.15,avg_[i],stdev_[i]) :

						close_.append(j)
						clsoe_stats.append("正态交易")
						values.append((close_1[j]-close_1[i])/close_1[i])
						zhengtai_value.append((close_1[j]-close_1[i])/close_1[i])
						zhengtai_count=zhengtai_count+1
						zhengtai_time.append(j-i)

						huiche.append((min(close_1[i:j])-close_1[i])/close_1[i])
						#print(5,len(open_),len(close_))
						break

					if (close_1[j]-close_1[i])/close_1[i]<-0.005:
				
						close_.append(j)
						clsoe_stats.append("止损订单")
						values.append((close_1[j]-close_1[i])/close_1[i])
						zhisun_value.append((close_1[j]-close_1[i])/close_1[i])
						zhisun_count=zhisun_count+1
						zhisun_time.append(j-i)
						huiche.append(0)
						#print(6,len(open_),len(close_))
						break


					if j>=len(lnA_B)-1:
						
						close_.append(-1)
						clsoe_stats.append(-1)		
						values.append(-1)
						huiche.append(0)	
			else:
				open_.append(0)
				close_.append(0)
				clsoe_stats.append(0)		
				values.append(0)
				huiche.append(0)		
		else:
			#print(3,len(open_),len(close_))
			open_.append(0)
			close_.append(0)
			clsoe_stats.append(0)		
			values.append(0)
			huiche.append(0)
		#print(len(open_),len(close_))
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
	#print(5,len(lnA_B),len(values),len(clsoe_stats),len(open_))
	#print(float(chenggonglv)*float(zhengtai_value1)+float(zhisun_value1)*float(1- float(chenggonglv)),chenggonglv,zhengtai_value1,zhisun_value1)
	writle_count(stockid_i[0]+","+str(zhengtai_count)+","+str(zhisun_count)+","+str(chenggonglv)+","+str(sum([abs(r-sum(lnA_B)/len(lnA_B)) for r in lnA_B])/len(lnA_B))+","+str(zhengtai_time1)+","+str(zhisun_time1)+","+str(zhengtai_value1)+","+str(zhisun_value1)+","+str(min(huiche))+","+str(float(chenggonglv)*float(zhengtai_value1)+float(zhisun_value1)*float(1- float(chenggonglv))))
	#print(stockid_i,stockid_j)
	##write_result(stockid_i,date1,time1,lnA_B,close_1,norm_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values,qushi_open_,qushi_close_,qushi_clsoe_stats)
def writle_count(word):
	print(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	file_object = open('count2.csv','a')
	file_object.write(word+"\n")
	file_object.close()
def writle_title():
	file_object = open('count2.csv','a')
	file_object.write("\n"+"ida,成功单数,失败单数,成功率,ln振幅,平均成功持仓时间,平均失败持仓时间,平均成功盈利,平均失败损失,最大回撤率,数学期望,顺势成功单数,顺势失败单数,顺势成功率,平均顺势成功时间,平均顺势失败时间,顺势最大回撤"+"\n")
	file_object.close()
def write_result(stockid_i,date1,time1,lnA_B,close_1,norm_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values,qushi_open_,qushi_close_,qushi_clsoe_stats):
	file_object = open('result.csv','w')

	file_object.write("id,stockid_i,date1,time1,lnA_B,close_1,norm_,avg_,stdev_,sample,commission,norm_num,open_,close_,clsoe_stats,values,qushi_open,qushi_close_,queshi_close_status"+"\n")
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
	#print(len(lnA_B),len(close_))
	print(len(lnA_B),len(close_),len(open_))
	for i in range(len(lnA_B)):
		#print(str(huiche[i]))
		file_object.write(str(i)+","+str(stockid_i[i])+","+str(date1[i])+","+str(time1[i])+","+str(lnA_B[i])+","+str(close_1[i])+","+str(norm_[i])+","+str(avg_[i])+","+str(stdev_[i])+","+str(sample)+","+str(commission)+","+str(norm_num)+","+str(open_[i])+","+str(close_[i])+","+str(clsoe_stats[i])+","+str(values[i])+"\n")
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
	norm_temp=[]
	avg_=[]
	stdev_=[]
	norm_lncha=[]
	res_all=0
	res_now=0
	sql="SELECT stockid FROM stock_foreign.stock_back   GROUP BY stockid ;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	#print(len(res))

	res_all=len(res)

	if len(res)>0:
		sql=""
		# sql="delete from model_data_model;"
		# cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
	
			print("第一次数据查询"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			sql2="select DISTINCT a.date,a.time,a.close from stock_back  a   where a.stockid='"+stockid[i]+"'   ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') "
			cur_stock.execute(sql2)
			res=cur_stock.fetchall()
			print("第二次数据查询"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			for r in res:
				try:
					stockid_i.append(stockid[i])

					lnA_B.append(float(r[2]))
					close_1.append(float(r[2]))
					date1.append(str(r[0]))
					time1.append(str(r[1]))
					#print(float(r[2]),float(r[3]),str(r[0]),str(r[1]))
					#print(math.log(float(r[2])))
					#print(math.log(float(r[3])))
				except Exception as e:
					print(str(r[1]),str(r[0]),"C端读入数据有问题")
			
			i_norm=0
			for r in range(0,len(close_1)):
				i_norm=i_norm+1
				if r>0:
					lnA_B_sub.append(lnA_B[r]-lnA_B[r-1])
					#print(lnA_B[r],lnA_B[r-1],lnA_B_sub[r])
				else:
					lnA_B_sub.append(lnA_B[0])
				
				if r>sample:
					norm_temp.append(scipy.stats.norm.cdf(lnA_B[r],sum(lnA_B[r-sample:r])/sample,stdev(lnA_B[r-sample:r])))
					norm_lncha.append(scipy.stats.norm.cdf(lnA_B_sub[r],sum(lnA_B_sub[r-sample:r])/sample,stdev(lnA_B_sub[r-sample:r])))
				else:
					norm_temp.append("")
					norm_lncha.append("")
				if i_norm>sample:
					#norm_lncha.append(scipy.stats.norm.cdf(lnA_B_sub[r],sum(lnA_B_sub[r-sample:r])/sample,stdev(lnA_B_sub[r-sample:r])))
					norm_.append(scipy.stats.norm.cdf(lnA_B[r],sum(lnA_B[r-sample:r])/sample,stdev(lnA_B[r-sample:r])))
					avg_.append(sum(lnA_B[r-sample:r])/sample)
					stdev_.append(stdev(lnA_B[r-sample:r]))
				else:
					norm_.append("")
					avg_.append("")
					stdev_.append("")
					#norm_lncha.append("")
				if norm_temp[r]!="" and norm_temp[r-1]!="" and norm_temp[r-2]!="" and norm_temp[r-3]!=""  and norm_temp[r-4]!="" and norm_temp[r-5]!="":
					if sum(norm_lncha[r-2:r])/len(norm_lncha[r-2:r])>0.9 or sum(norm_lncha[r-2:r])/len(norm_lncha[r-2:r])<0.1 :
					#if abs(max(norm_temp[r],norm_temp[r-1],norm_temp[r-2],norm_temp[r-3],norm_temp[r-4])-min(norm_temp[r],norm_temp[r-1],norm_temp[r-2],norm_temp[r-3],norm_temp[r-4]))>0.6:
						i_norm=0


			print("第一次计算"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			if len(close_1)>=sample:
			
				run(stockid_i,date1,time1,lnA_B,lnA_B_sub,close_1,norm_,avg_,stdev_,sample,commission,norm_num,norm_lncha,norm_temp)

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
			print("第一次计算完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
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
			norm_temp=[]
			norm_lncha=[]
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


	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()
	cur_result=conn.cursor()
	cur_d=conn.cursor()
	cur_check=conn.cursor()
	cur_result_DB=conn.cursor()
	cur_stock_releation=conn.cursor()
	writle_title()
	data_clear(100,0.0005,0.9)








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

