# CVClient.py
# Computer Vision Client Class for LucidTronix eLucidator Applications
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import socket
import pygame
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO
from time import time, sleep
from picamera import PiCamera
from TouchScreen import TouchScreen
from LucidApp import LucidApp, Button
from picamera.array import PiRGBArray
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

MSG_LEN = 16
PORT = 8421

class CVClient(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(800, 400), 
					icon_path='./icons/cv_client.png', base_graphics='cv2'):
		super(CVClient, self).__init__('CVClient', cache_path, fullscreen, resolution, icon_path, base_graphics)
		self.playing = True
		self.stream = ImageStreamDir()
		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()

		self.camera = PiCamera()
		self.camera.resolution = (320, 240)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
		self.faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
		self.pil_im_to_classify = Image.open('./images/baby.jpg')
		self.classifications = []

		self.buttons.append(Button(self, 'classify', (100,10,125,40), (50,50,50), self.classify_pil_im))


		# allow the camera to warmup
		sleep(0.2)

	def __str__(self):
		return 'CVClient'

	def run(self):

		while True:
			self.ts.update()

			# capture frames from the camera
			for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
				image = frame.array
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				faces = self.faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
				
				# Draw a rectangle around the faces
				for (x, y, w, h) in faces:
					cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)


				self.show_image_cv(image, (20,70))
				#self.show_image(image)

				# clear the stream in preparation for the next frame
				self.rawCapture.truncate(0)

				for b in self.buttons:
					if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
						print 'Try to press button:', b.name
						ret = b.press() 
						if ret < 0:
							print 'Quit CV Client on buttons'
							return ret
						self.ts.double_tap = False
					b.show()

				ret = self.handle_keys()
				if ret <= 0:
					return ret

				self.draw()
	
	def classify_pil_im(self):
		print 'Try classification:'
		ct = ClassificationThread(self.pil_im_to_classify, self.classifications)
		print 'Made ct thread'
		ct.start()
		return 0

class ClassificationThread(threading.Thread):
	def __init__(self, image, classifications):
		threading.Thread.__init__(self)
		self.image = image
		self.classifications = classifications

	def run(self):
		print 'In ct run'

		self.send_image()
		sleep(3.0)
		self.receive_classification()		
		print "Exiting classification thread."

	def send_image(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('Connecting client at:', ('192.168.2.9', PORT))
		sock.connect(('192.168.2.9', PORT))
		print "Starting ethernet client image send:"
		rgb_im = self.image.convert('RGB')
		img_str = rgb_im.tostring()
		
		# First send image size then send image
		try: 
			img_len = str(len(img_str)) + " " + str(rgb_im.size[0]) + " " + str(rgb_im.size[1])
			img_len = img_len.ljust(MSG_LEN)
			sock.sendall(img_len)
			data = ''
			while len(data) == 0:
				data = sock.recv(4096)
			print ' Server received ',data,' Now sending image size:', img_len
			sock.sendall(img_str)
		finally:
			sock.close()

		print "Clasification thread sent the image."

	def receive_classification(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('192.168.2.9', PORT))
		print "Starting ethernet client classification receive..."

		try:
			sock.sendall("0 640 480".ljust(MSG_LEN))
			classification = ''
			while len(classification) == 0:
				classification = sock.recv(4096)
			print 'Server classification:', classification
			self.classifications.append(classification)
		finally:
			sock.close()


if __name__ == '__main__':
	app = CVClient()
	app.run()
