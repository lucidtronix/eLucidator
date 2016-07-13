# Slideshow.py
# Slideshow Class for LucidTronix eLucidator Applications
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import threading
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from LucidApp import LucidApp
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class Slideshow(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(500, 400), 
					icon_path='./icons/slideshow.png', base_graphics='cv2'):
		super(Slideshow, self).__init__('ImageSlider', cache_path, fullscreen, resolution, icon_path, base_graphics)
		self.playing = True
		self.stream = ImageStreamDir(load_strategy='paths')

		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()

		self.delay = 5.0 #seconds
		self.last_update = time() - self.delay

	def __str__(self):
		return 'Slideshow'

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
				print 'Try to show next image.'
				cur_img = self.stream.next()
				self.show_image(cur_img)
				self.last_update = time()

			self.draw()



if __name__ == '__main__':
	app = Slideshow()
	app.run()