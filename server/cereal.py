#!/usr/bin/env python3
import serial
import serial.tools.list_ports

def list_ports():
	ports=[]
	for port in serial.tools.list_ports.comports():
		if port[1]!='n/a':
			ports.append(port[0])
	return ports

class auto_port_t:
	def __init__(self,baud=115200):
		self.baud=baud
		self.obj=None

	def connected(self):
		return self.obj!=None and self.obj.isOpen()

	def connect(self):
		self.close()

		ports=list_ports()

		if len(ports)<=0:
			return False

		try:
			self.obj=serial.Serial(port=ports[0],baudrate=self.baud)

			if not self.connected():
				self.close()
				return False

			return True

		except Exception as error:
			print(error)
			return False

	def close(self):
		if self.connected():
			self.obj.close()
			self.obj=None

	def write(self,data):
		if self.connected():
			try:
				self.obj.write(data)
			except Exception as error:
				self.close()
				print(error)
