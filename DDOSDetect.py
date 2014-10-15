# encoding:utf-8
from mod.fileHandler import fileHandler
from Queue import Queue
from time import sleep,strftime,localtime
class AccessInfo:
	def __init__(self,dip):
		self.dip = dip
		self.time = []
		self.sip = []
		self.count = 0		
		self.period_start = -1
		self.period = -1


#AccessDict 
class DDOSDetect:
	def __init__(self,period,number):
		self.period =  period
		self.number = number
		self.period_start = -1
		self.AccessDict = {}
		self.result = []

	def handleDate(self,metaQue):
		while not metaQue.empty():
			tmp = metaQue.get()
			access = None
			if(self.period_start==-1):
				self.period_start = int(round(float(tmp.timestamp)))
				access = AccessInfo(tmp.dip)
				access.time.append(tmp.timestamp)
				access.period = self.period
				access.period_start = self.period_start
				access.sip.append(tmp.sip)
				access.count = access.count + 1
				self.AccessDict[tmp.dip+str(self.period_start)] = access
			elif(self.period_start+self.period>int(round(float(tmp.timestamp)))):
				if self.AccessDict.has_key(tmp.dip+str(self.period_start)) and self.period_start==self.AccessDict[tmp.dip+str(self.period_start)].period_start :
					access = self.AccessDict[tmp.dip+str(self.period_start)]
					access.sip.append(tmp.sip)
					access.time.append(tmp.timestamp)
					access.count = access.count + 1
				else:
					access = AccessInfo(tmp.dip)
					access.time.append(tmp.timestamp)
					access.period = self.period
					access.period_start = self.period_start
					access.sip.append(tmp.sip)
					access.count = access.count + 1
					self.AccessDict[tmp.dip+str(self.period_start)] = access
			elif(self.period_start+self.period<=int(round(float(tmp.timestamp)))):
				self.period_start = self.period_start + self.period
				access = AccessInfo(tmp.dip)
				access.time.append(tmp.timestamp)
				access.period = self.period
				access.period_start = self.period_start
				access.sip.append(tmp.sip)
				access.count = access.count + 1
				self.AccessDict[tmp.dip+str(self.period_start)] = access

	def scan(self,metaQue):
		self.handleDate(metaQue)
		for key,value in self.AccessDict.items():
			if value.count > self.number:
				self.result.append(value)
		return self.result


if __name__ == '__main__':
	fileQue = Queue()
	fileQue.put("m20130301/0122.log",True)
	metaQue = Queue()
	x = fileHandler(fileQue,metaQue)
	x.start()
	sleep(10)
	test = DDOSDetect(2,100)
	print metaQue.qsize()
	result = test.scan(metaQue)
	print len(test.AccessDict)
	f = open("tmp.txt","w")
	for tmp in result:
		f.write("dip:%s,count:%d,period:%d-%d\n"%(tmp.dip,tmp.count,tmp.period_start,tmp.period_start+tmp.period))
		for i in range(0,len(tmp.sip)):
			ltime = localtime(float(tmp.time[i]))
			f.write("time:%s,ip:%s\n"%(strftime("%Y/%m/%d %H:%M:%S",ltime),tmp.sip[i]))
		f.write("-----------------------------------------\n")
			
		# f.write("ip:%s\n"%tmp.dip)
		# f.write("period:%d-%d"%(tmp.period_start,tmp.period))
		# f.write("sip:\n")
		# for sip in tmp.sip:
		# f.write("ip:"+sip+"\n")
			
	
	

