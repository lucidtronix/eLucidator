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
from ImageStreamDir import ImageStreamDir


class ImageSlider(LucidApp):
	def __init__(self, cache_path='./', fullscreen=true, resolution=(500, 400), icon=None, base_graphics='pygame'):
		super(ImageSlider, self).__init__('ImageSlider', cache_path, fullscreen, resolution, icon, base_graphics)
		self.playing = True
		self.stream = ImageStreamDir()

	def __str__(self):
		return super(ImageSlider, self).__str__() + 'Playing:' + str(self.playing)

	def open(self):
		pass

	def close(self):
		pass

	def run(self):
		sliding = False
		sx = sy = dx = cx = 0
		b0_begin = b1_begin = 0
		last_hold = last_up = 1.0
		cur_img = self.stream.next()

		while True:
			self.surface.fill(0)
			mx, my = pygame.mouse.get_pos()
			b1, b2, b3 = pygame.mouse.get_pressed()

			if b1:
				if not sliding:
					last_up = time()-b0_begin 
					b1_begin = time()
					sliding = True
					sx = mx
					sy = my
				dx = mx - sx
			elif sliding:
				cx = cx+dx
				dx = 0
				sliding = False
				hold_time = time()-b1_begin
				if 0.01 < last_hold < 0.3 and 0.01 < last_up < 0.3 and 0.01 < hold_time < 0.3:
					cur_img = self.stream.next()

				last_hold = hold_time
				b0_begin = time()

			self.surface.blit(cur_img, (cx+dx,10))

			self.label("B1:"+str(b1)+"  B2:"+str(b2) + "   B3:"+str(b3), 10, 30)
			self.label("MX:"+str(mx)+"  MY:"+str(my), 10, 50)
			self.label("Last Hold:"+str(last_hold)+"  MY:"+str(my), 10, 70)

			pygame.display.update()
		
			old_b1 = b1

			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					return 0
				elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return 0