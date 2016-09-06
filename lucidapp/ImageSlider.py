# ImageSlider.py
# ImageSlider Class for LucidTronix eLucidator Applications
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
from ImageRow import ImageRow
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class ImageSlider(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(800, 400), 
					icon_path='./icons/image_slider.png', base_graphics='cv2'):
		super(ImageSlider, self).__init__('ImageSlider', cache_path, fullscreen, resolution, icon_path, base_graphics)

		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()

		self.playing = True
		self.stream = ImageStreamDir()
		self.stream.next()

		self.row = ImageRow(self, self.stream, self.ts, self.resolution)

	def __str__(self):
		return 'ImageSlider'

	def open(self):
		pass

	def close(self):
		pass

	def run(self):

		while True:
			self.ts.update()
			self.row.update()
			self.row.display()


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
			self.draw()


if __name__ == '__main__':
	app = ImageSlider()
	app.run()