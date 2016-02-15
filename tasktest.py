import os
import time




def getInfo(processname):             #通过tasklist命令，找到processname的pid
	task = os.popen('tasklist')
	if processname in task.read():
		print(1)
		num = os.popen('wmic process where name="'+processname+'" get CommandLine')
		#print( num.read().split("\n"))
		#print(num.read().split("\n")[2].index("E:\BaiduYunDownload\phpStudy\WWW\\forlining\\task.py"))
		for r in num.read().split("\n"):
			if r.strip()!='':

				word="E:\BaiduYunDownload\phpStudy\WWW\\forlining\\task.py"
				if r.find("C:\github\stock2015\process_1.2.py")!=-1:
					print(666)
				if r.find("C:\github\stock2016forlmx\process_1.2_forlmx.py")!=-1:
					print(777)


if __name__ == '__main__':
	print(getInfo("python.exe"))