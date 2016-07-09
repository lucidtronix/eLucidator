# FaceDetector.py
# FaceDetector Class for LucidTronix eLucidator Applications
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO
from time import time, sleep
from LucidApp import LucidApp
from picamera import PiCamera
from TouchScreen import TouchScreen
from picamera.array import PiRGBArray
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class FaceDetector(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(500, 400), icon=None, base_graphics='cv2'):
		super(FaceDetector, self).__init__('FaceDetector', cache_path, fullscreen, resolution, icon, base_graphics)
		self.playing = True
		self.stream = ImageStreamDir()
		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()
		self.camera = PiCamera()
		self.camera.resolution = (320, 240)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(camera, size=(320, 240))
		self.faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

        # allow the camera to warmup
		sleep(0.2)

	def __str__(self):
		return 'FaceDetector'

	def run(self):

		while True:
			self.ts.update()


			# capture frames from the camera
			for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
				image = frame.array
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
				
				# Draw a rectangle around the faces
				for (x, y, w, h) in faces:
					cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)

				for b in self.buttons:
					if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
						ret = b.press() 
						if ret < 0:
							return ret
						self.ts.double_tap = False
					b.show()

				self.show_image(image)
				self.draw()

				# clear the stream in preparation for the next frame
				rawCapture.truncate(0)

				ret = self.handle_keys()
				if ret <= 0:
					return ret


if __name__ == '__main__':
	app = FaceDetector()
	app.run()