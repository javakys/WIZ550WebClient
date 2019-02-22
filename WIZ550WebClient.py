#!/usr/bin/python

import sys
import socket
import time

if sys.version_info > (3, 0):
	import http.client
	import urllib.request, urllib.parse
else:
	import httplib, urllib

	
class WIZ550WebClient:
	def __init__(self, host):
		import logging
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger()
		
		self.conn = None
		self.host = host
		self.paramsdic = {}
		self.inputs = []
		for i in range(16):
			self.inputs.append(0)
		

	def getGINstateall(self):
		import json
	
		try:	
			if sys.version_info > (3, 0):
				self.conn = http.client.HTTPConnection(self.host, timeout=1)
				
			else:
				self.conn = httplib.HTTPConnection(self.host)

			self.conn.connect()
			self.conn.request("GET", "/io.cgi")
			r2 = self.conn.getresponse()
			data = r2.read()
			index = data.find("(", 0, len(data))
			index2 = data.find(")", index, len(data))
			j = json.loads(data[index+1:index2])

			for i in range(16):
				self.inputs[i] = j['din'][i]['v']

		except Exception as e:
			# sys.stdout.write('%r\r\n' % e)
			return False
		finally:
			self.conn.close()		

	def getGINstate(self, portnum):
		import json
		
		if sys.version_info > (3, 0):
			self.conn = http.client.HTTPConnection(self.host, timeout=1)
		else:
			self.conn = httplib.HTTPConnection(self.host)
		self.conn.connect()
		self.conn.request("GET", "/io.cgi")

		r2 = self.conn.getresponse()
		data = r2.read()
		index = data.find("(", 0, len(data))
		index2 = data.find(")", index, len(data))
		j = json.loads(data[index+1:index2])
		
		retval = j['din'][portnum]['v']
		
		return retval
		
	def setGOUTvalue(self, portnum, value):
#		print('portnum: ', portnum)
#		print('value: ', value)
		
		self.paramsdic['val'] = value
		self.paramsdic['pin'] = portnum


		while True:
			try:		
#				params = urllib.urlencode({'val': 0, 'pin': 8})
				if(sys.version_info > (3, 0)):
					params = urllib.parse.urlencode(self.paramsdic)
				else:
					params = urllib.urlencode(self.paramsdic)
				headers = {"Content-type": "application/x-www-form-urlencoded", 
			  		 		"Accept": "text/plain"}	

#				print('Send httpconnection')
				if(sys.version_info > (3, 0)):
					self.conn = http.client.HTTPConnection(self.host, timeout=1)
				else:
					self.conn = httplib.HTTPConnection(self.host)
				self.conn.connect()
				self.conn.request("POST", "/dout.cgi", params, headers)	
#				time.sleep(0.1)
				r2 = self.conn.getresponse()
			
#				print r2.status, r2.reason
				
				if(r2.status == 200):
					break
					
				r2.status = 0
				r2.reason = ''
				return True
			except Exception as e:
				# sys.stdout.write('%r\r\n' % e)
				return False
		
			finally:	
				self.conn.close()


if __name__ == '__main__':
	webclient = WIZ550WebClient("192.168.11.100")
	value = 1
	
	while True:
		for i in range(0, 16):
			if (i < 4 or i > 7):
				webclient.setGOUTvalue(i, value)
				time.sleep(3)
		
		value = (value + 1) % 2
		time.sleep(1)
	
