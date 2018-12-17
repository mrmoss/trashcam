#!/usr/bin/env python3
import camera
import cereal
import http.server
import mimetypes
import os
import selectors
import struct
import time
import urllib.parse

#Global webcam object (change this to which camera dev your camera is)
cam=camera.autocam(1)

#Global serial port object
serial_port=cereal.auto_port_t()

#Generates a packet to send to serial port with given values
def gen_move_packet(roll,yaw,light):
	payload=struct.pack('<hhB',roll,yaw,light)

	crc=0
	for bb in payload:
		crc^=bb

	HEADER_SIG=0x33
	MOVE_SIG=0x01
	return struct.pack('<BBB',HEADER_SIG,MOVE_SIG,len(payload))+payload+struct.pack('<B',crc)

#Custom handler
class handler(http.server.BaseHTTPRequestHandler):

	def version_string(self):
		return ''

	def send_error(self,code,message=None,explain=None):
		self.send_response(code)
		self.end_headers()

	def log_message(self,format,*args):
		return

	def parse_uri(self):
		#Parse and and query
		self.path=self.path.split('?')
		self.queries='?'.join(self.path[1:])
		if len(self.queries)>0:
			self.queries='?'+self.queries
		self.path=self.path[0]
		self.queries=urllib.parse.parse_qs(urllib.parse.urlparse(self.queries).query)
		for key in self.queries:
			self.queries[key]=self.queries[key][-1]

		#Default '/' to '/index.html'
		if len(self.path)>0 and self.path[-1]=='/':
			self.path+='index.html'

	def do_GET(self):
		try:
			#Separate path and query string
			self.parse_uri()

			#Ensure resource is in web directory
			cwd=os.getcwd()+'/web/'
			self.path=os.path.abspath(cwd+self.path)
			if self.path.find(cwd)!=0 or not os.path.isfile(self.path):
				self.send_error(404)
				return

			#Read file
			fd=open(self.path,'rb')
			data=fd.read()
			fd.close()

			#Figure out mimetype
			mime=mimetypes.guess_type(self.path)
			if len(mime)>0:
				mime=mime[0]
			else:
				mime='text/plain'

			#Send file
			self.send_response(200)
			self.send_header('Content-type',mime)
			self.end_headers()
			self.wfile.write(data)

		#If anything bad happens send a 401 unauthorized
		except Exception as error:
			self.send_error(401)

	def do_POST(self):
		try:
			#Separate path and query string
			self.parse_uri()

			#Parse commands
			global serial_port
			roll=0
			yaw=0
			speed=10
			light=1
			if 'l' in self.queries:
				yaw+=1
			if 'r' in self.queries:
				yaw-=1
			if 'u' in self.queries:
				roll+=1
			if 'd' in self.queries:
				roll-=1
			if 'f' in self.queries:
				light=0
			serial_port.write(gen_move_packet(roll*speed,yaw*speed,light))

			#Parse camera command
			global cam
			data=b''
			if 'i' in self.queries:
				data=cam.get_jpg()

			#Send data
			self.send_response(200)
			self.send_header('Content-type','application/octet-stream')
			self.end_headers()
			self.wfile.write(data)

		#If anything bad happens send a 401 unauthorized
		except Exception as error:
			self.send_error(401)

if __name__=='__main__':
	while True:
		try:
			#Create http server
			server=http.server.HTTPServer(('127.0.0.1',8081),handler)

			#Choose selector for http polling
			if hasattr(selectors,'PollSelector'):
				selector_type=selectors.PollSelector
			else:
				selector_type=selectors.SelectSelector

			#Event loop
			while True:

				#Keep camera connected
				if not cam.connected():
					time.sleep(1)
					cam.connect()

				#Keep serial port connected
				if not serial_port.connected():
					time.sleep(1)
					serial_port.connect()

				#Serve http clients
				with selector_type() as selector:
					selector.register(server,selectors.EVENT_READ)
					if selector.select(0.5):
						server._handle_request_noblock()
					server.service_actions()

				#Give cpu a break
				time.sleep(0.00001)

		#Ctrl+c
		except KeyboardInterrupt:
			exit(-1)

		#Unexpected error
		except Exception as error:
			print(error)
