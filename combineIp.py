#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import struct
import copy
import sys

#二进制IP地址转化成封装点分十进制IP地址
def ipNtoA(in_addr):
	return socket.inet_ntoa(struct.pack('!L', in_addr))


#IP地址类
class IP_Address(object):
	def __init__(self, ip, mask):
		self.ip = ip
		self.mask = mask

	#点分十进制IP转化成地址二进制IP地址	
	def ipAtoN(self):
		return struct.unpack("!L", socket.inet_aton(self.ip))[0]

	#判断根据mask移位后的IP地址是否为偶数
	def isEvenNumber(self):
		ipadd = self.ipAtoN()
		ipadd = ipadd >> (32 - self.mask)

		if ipadd % 2 == 0 :
			#print socket.inet_ntoa(struct.pack('!L', ipadd)) + '/%s' %self.mask
			return True
		else:
			return False
		


#IP list 列表类
class IP_List(object):

	def __init__(self):
		self.list = []

	def WriteFile(self, filename):
		text = open(filename,'w')
		for index in range(len(self.list)):
			#print self.list[index].ip + "/%s" %self.list[index].mask
			text.write(self.list[index].ip + "/%s" %self.list[index].mask)
			text.write('\n')

		text.close()
	#按行读取文件中的内容	
	def readFile(self, filename):
			text=open(filename)

			line = text.readlines()
			text.close()
			return line

	#展开IP地址
	def ipDeploy(self, Ipcontext):
		for member in Ipcontext:
			if member == '\n':
				continue

			str_ip=member.strip('\r\n')
			if "-" in str_ip:
				str_hip, str_eip= str_ip.split('-')
				#print str_hip, str_eip
				hip = struct.unpack("!L", socket.inet_aton(str_hip))[0]
				eip = struct.unpack("!L", socket.inet_aton(str_eip))[0]

				while hip <= eip:
					#print hip
					#print socket.inet_ntoa(struct.pack('!L', hip)) 
					hip_str = ipNtoA(hip)
					ipadd = IP_Address(hip_str, 32)
					self.list.append(ipadd)
					#IpList.append(socket.inet_ntoa(struct.pack('!L', hip)))
					#print IpList
					hip = hip + 1
			else:
				if "/" in str_ip:
					ip,mask = str_ip.split('/')
					ipadd = IP_Address(ip, int(mask))
					self.list.append(ipadd)
				else:
					ipadd = IP_Address(str_ip, 32)
					self.list.append(ipadd)


	def deleteRepeateIP(self, Ipcontext):
		iplist = list(set(Ipcontext))
		#print iplist
		return iplist

	#将从文件中读出的IP地址对象放入list列表中
	def insertIpAddressToList(self, filename):
		Ipcontext = self.readFile(filename)
		Ipcontext = self.deleteRepeateIP(Ipcontext)
		#print Ipcontext
		self.ipDeploy(Ipcontext)

	#显示IPlist 列表的内	容			
	def showIpList(self):
		for index in range(len(self.list)):
			print self.list[index].ip + "/%s" %self.list[index].mask

	#根据IP地址的大小进行排序
	def ipSort(self):
		self.list = sorted(self.list, key = lambda IP_Address: IP_Address.ipAtoN())

	def combineIpAddress(self):
		ini_len = len(self.list)
		index = 0

		while index < len(self.list) - 1:
			if self.list[index].isEvenNumber():
				if self.list[index + 1].mask == self.list[index].mask:
					mask = self.list[index].mask
					pre_ip = self.list[index].ipAtoN()
					next_ip = self.list[index + 1].ipAtoN()
					pre_ip  = pre_ip >> (32 - mask)
					next_ip = next_ip >> (32 - mask)
					if pre_ip + 1 == next_ip:
						self.list[index].mask = self.list[index].mask - 1
						self.list.pop(index + 1)
			index = index + 1

		if ini_len == len(self.list):
			return
		else:
			print '*********'
			self.combineIpAddress()



		#print iplist
#设计思想：
#1.第一个IP的从高位到低位掩码位数的整数值一定是偶数。例如：x.x.x.200/31 = |xxxxx1100100|0 "|"包扩的31位的值为偶数
#2.判断合并后的IP网段是否跟下一个IP是相同的掩码，掩码相同才可以合并。
#3.移位，删除不关心的位，存在移位后的下一个IP值比该移位后的偶数IP大1，则这两个IP地址可以合并为一个网段，掩码减一（例如10.1.1.2和10.1.1.3）
#4.IP合并成一个网段之后，删除奇数IP
#5.循环重复2操作，只进行两个IP的合并
#6.第一次函数循环表示完成了IPlist的两个两个的合并，然后递归的再进行两个两个IP的合并，直到合并后IPlist的长度不在变化结束。

#200 11001000/32 
#               \
#                11001000/31 ---判断从左往右 --是-> 1100100
#                           mask这么多位是否为偶数        \
#               /                                          \
#201 11001001/32                                            \
#                                                            1100100/30---右移一位---> 110010
#202 11001010/32                                            /                            \
#               \                                          /                              \
#                11001010/31 ---（index + 1）--是-> 1100101                                \
#                           右移一位是否比index的IP大1                                      \
#               /                                                                            \
#203 11001011/32                                                                              \                   
#                                                                                            110010/29 --- 右移一位 --  11001 为奇数 不可以合并了                        
#204 11001100/32                                                                              /
#               \                                                                            /
#                11001100/31 ---判断从左往右 --是-> 1100110                                 /
#                           mask这么多位是否为偶数        \                                /
#               /                                          \                              /
#205 11001101/32                                            \                            / 
#                                                            1100110/30---右移一位---> 110011
#206 11001110/32                                            /                             
#               \                                          /                               
#                11001110/31 ---（index + 1）--是-> 1100111                                 
#                           右移一位是否比index的IP大1                                       
#               /        
#207 11001111/32                                                                              
#
#208 11010000/32                                                                            
#               \
#                11010000/31 ---判断从左往右 --是-> 1101000
#                           mask这么多位是否为偶数        \
#               /                                          \
#209 11010001/32                                            \
#                                                            1101000/30---右移一位---> 110100
#210 11010010/32                                            /                            \          
#               \                                          /                              \             
#                11010010/31 ---（index + 1）--是-> 1101001                                \
#                           右移一位是否比index的IP大1                                      \                
#               /                                                                            \                                      
#211 11010011/32                                                                              \
#                                                                                            110100/29 --- 右移一位 --  11010 为偶数，但是index+1掩码不同，不能合并                                                                      
#212 11010100/32                                                                              /
#               \                                                                            /
#                11010100/31 ---判断从左往右 --是-> 1101010                                 /        
#                           mask这么多位是否为偶数        \                                /            
#               /                                          \                              /            
#213 11010101/32                                            \                            /          
#                                                            1101010/30---右移一位---> 110101
#214 11010110/32                                            /
#               \                                          / 
#                11010110/31 ---（index + 1）--是-> 1101011
#                           右移一位是否比index的IP大1 
#               /
#215 11010111/32

#216 11011000/32----------------------------------------------------------------------------11011000/32

					


if __name__ == '__main__':

	listip = IP_List()
        filename = sys.argv[1]
	listip.insertIpAddressToList(filename)
	#listip.showIpList()
	listip.ipSort()

	listip.combineIpAddress()
	#listip.WriteFile('C:\Users\yeruoxi\Desktop\\txt\\result2.txt')
	listip.showIpList()


