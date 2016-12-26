# Slideshow.py
# Slideshow Class for LucidTronix eLucidator Applications
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import defines
import threading
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from TouchScreen import TouchScreen
from LucidApp import LucidApp, Button
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class Slideshow(LucidApp):
	def __init__(self, ts=None, cache_path=defines.base_path+'cache/', fullscreen=False, resolution=(800, 400), 
					icon_path=defines.base_path+'icons/slideshow.png', base_graphics='cv2'):
		super(Slideshow, self).__init__('Slideshow', cache_path, fullscreen, resolution, icon_path, base_graphics)
		self.playing = True
		self.stream = ImageStreamDir(load_strategy='paths')
		
		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()

		self.delay = 5.0 # seconds
		self.last_update = time() - self.delay
		self.fading = False
		self.fade_time = 2.0 # seconds
		self.fade_start = time()
		self.last_image = None
		self.cur_image = None
		self.image_corner = (30,90)

		self.buttons.append(Button(self, 'next', (260,10,80,40), (50,50,50), self.next))
		self.buttons.append(Button(self, 'previous', (100,10,145,40), (50,50,50), self.prev_image))


	def __str__(self):
		return 'Slideshow'

	def next_image(self):
		self.last_image = self.cur_image
		if self.last_image is not None:
			self.fading = True
			self.fade_start = time()
		self.cur_image = self.stream.next()
		self.last_update = time()		

	def prev_image(self):
		self.last_image = self.stream.prev()
		self.cur_image = self.last_image
		self.last_update = time()
		return 0	

	def run(self):
		cx = oldx = 0
		pic_update = 0

		while True:
			self.ts.update()

			ret = self.handle_keys()
			if ret <= 0:
				return ret

			for b in self.buttons:
				if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press() 
					if ret < 0:
						return ret
					self.ts.double_tap = False
				b.show()

			if time()-self.last_update > self.delay:
				self.next_image()

			if self.fading:
				alpha =	(time()-self.fade_start) / self.fade_time 
				if alpha > 1.0:
					self.fading = False

				beta = (1.0 - alpha)
				blend = cv2.addWeighted(self.last_image.to_array(), beta, self.cur_image.to_array(), alpha, 0.0)
				self.show_image_cv(blend, self.image_corner)
			else:
				self.show_image(self.cur_image, self.image_corner)
			self.draw()

	def next(self):
		self.next_image()
		self.fading = False
		return 0

if __name__ == '__main__':
	app = Slideshow()
	app.run()