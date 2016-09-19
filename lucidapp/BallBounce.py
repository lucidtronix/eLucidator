# BallBounce.py
# BallBounce Class for LucidTronix eLucidator
# Samwell Freeman
# September 2016

import os
import sys
import cv2
import math
import pygame
import threading
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from LucidApp import LucidApp, Button
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir

class BallBounce(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, 
					resolution=(800, 400), icon_path='./icons/BallBounce.png'):
		
		super(BallBounce, self).__init__('BallBounce', cache_path, fullscreen, resolution, icon_path)
		
		self.ts = ts if ts else TouchScreen()
		self.last_update = time() 
		#self.buttons.append(Button(self, 'next', (260,10,80,40), (50,50,50), self.next))
		#self.buttons.append(Button(self, 'previous', (100,10,145,40), (50,50,50), self.prev_image))
		self.cur_color = (128,128,128)
		self.bg_color = (0,0,0)

	def __str__(self):
		return 'BallBounce'


	def run(self):
		num_samples = 60
		offset = 70
		sample_matrix = np.random.rand(2, num_samples)
		sample_matrix[0,:] *= self.resolution[0]-offset
		sample_matrix[1,:] *= self.resolution[1]-offset
		sample_matrix += offset

		deltas = np.random.randn(2, num_samples) / 3.0


		sample_sizes = np.random.randint(4, 15, num_samples)
		sample_colors = np.random.randint(255, size=(num_samples, 3))

		quit = False
		while not quit:
			self.fill()
			self.ts.update()

			ret = self.handle_keys()
			if ret < 0:
				quit = True

			for b in self.buttons:
				if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press() 
					if ret < 0:
						quit = True
					self.ts.double_tap = False
				b.show()
			
			if self.ts.sliding:
				cv2.circle(self.canvas, (self.ts.mx, self.ts.my), 2, self.cur_color, -1)
				draw_spiral(self.canvas, self.ts.mx, self.ts.my, 12)

			out = sample_matrix[0,:] > self.resolution[0]
			deltas[0,:][out] = -deltas[0,:][out]
			out = sample_matrix[1,:] > self.resolution[1]
			deltas[1,:][out] = -deltas[1,:][out]	
			out = sample_matrix < offset
			deltas[out] = -deltas[out]
			sample_matrix += deltas

			for i in range(sample_matrix.shape[1]):
				sc = (sample_colors[i][0], sample_colors[i][1], sample_colors[i][2])
				cv2.circle(self.canvas, (int(sample_matrix[0][i]), int(sample_matrix[1][i])), sample_sizes[i], sc, -1)

			self.draw()



def draw_spiral(canvas, x, y, radius):

	sradius = radius
	rfac = 2
	for theta in np.arange(0.0, 20.0*math.pi, 0.4):
		ct = math.cos(theta)
		st = math.sin(theta)
		sx = x + ct * sradius
		sy = y + st * sradius

		scolor = (255, int(128 + 127*ct), int(128 + 127*st))
		cv2.circle(canvas, (int(sx), int(sy)), 4, scolor, -1)
		sradius += rfac

if __name__ == '__main__':
	app = BallBounce()
	app.run()
