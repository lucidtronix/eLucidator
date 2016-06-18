# LucidApp.py
# Base Class for LucidTronix eLucidator Applications
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
from ImageStreamInstagram import ImageStreamInstagram
from TouchScreen import TouchScreen

class InstagramSlider(LucidApp):
	def __init__(self, cache_path='./', fullscreen=False, resolution=(500, 400), icon=None, base_graphics='pygame'):
		super(InstagramSlider, self).__init__('InstagramSlider', cache_path, fullscreen, resolution, icon, base_graphics)
		self.playing = True
		self.stream = ImageStreamInstagram(user='samwell3')
		self.ts = TouchScreen()

	def __str__(self):
		return super(InstagramSlider, self).__str__() + 'Playing:' + str(self.playing)

	def open(self):
		pass

	def close(self):
		pass

	def run(self):
		cx = oldx = 0
		pic_update = 0
		cur_img = self.stream.next()
		self.surface.blit(cur_img, (cx,10))

		while True:
			self.ts.update()
			mx, my = pygame.mouse.get_pos()
			b1, b2, b3 = pygame.mouse.get_pressed()

			if self.ts.sliding:
				cx = oldx + self.ts.delta[0]
				self.surface.fill(0)
				self.surface.blit(cur_img, (cx,10))
				pygame.display.update()

			else:
				oldx = cx

			if self.ts.double_tap and time()-pic_update > 0.6:
				cur_img = self.stream.next()
				pic_update = time()
			
				self.surface.blit(cur_img, (cx,10))

				self.label("B1:"+str(b1)+"  B2:"+str(b2) + "   B3:"+str(b3), 10, 30)
				self.label("MX:"+str(mx)+"  MY:"+str(my), 10, 50)
				self.label("Last Hold:"+str(self.ts.last_hold), 10, 70)
				self.label("Double Tap:"+str(self.ts.double_tap), 10, 90)

				pygame.display.update()

			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					return 0
				elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return 0