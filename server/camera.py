#!/usr/bin/env python3
import cv2

class autocam_t:
	def __init__(self,num=0):
		self.num=num
		self.obj=None

	def connected(self):
		return self.obj!=None and self.obj.isOpened()

	def connect(self):
		try:
			self.close()
			self.obj=cv2.VideoCapture(self.num)
			self.obj.set(cv2.CAP_PROP_FRAME_WIDTH,640)
			self.obj.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
			self.obj.set(cv2.CAP_PROP_FRAME_COUNT,0)
		except Exception as error:
			pass

	def close(self):
		if self.connected():
			self.obj.release()
			self.obj=None

	def get_jpg(self):
		try:
			status,img=self.obj.read()
			if not status:
				raise Exception('Could not read camera.')

			status,data=cv2.imencode('.jpg',img)
			if not status:
				raise Exception('Could not decode image.')

			return data.tostring()

		except Exception as error:
			self.close()
			return b''