# TouchScreen.py
# TouchScreen for LucidTronix eLucidator
# Samwell Freeman
# June 2016

import pygame
from time import time

class TouchScreen:
	def __init__(self):
		self.start = (0,0)
		self.delta = (0,0)
		self.last_hold = 0
		self.last_up = 0
		self.up = 0
		self.hold = 0
		self.sliding = False
		self.double_tap = False
		self.double_tap_time = 0
	def update(self):
		mx, my = pygame.mouse.get_pos()
		b1, b2, b3 = pygame.mouse.get_pressed()

		if b1:
			self.double_tap = False
			if not self.sliding:
				self.last_up = time()- self.up
				self.last_hold = self.hold
				self.hold = time()
				self.sliding = True
				self.start = (mx, my)
			self.delta = (mx - self.start[0], my - self.start[1])
		elif self.sliding:
			self.delta = (0,0)
			self.sliding = False
			self.hold = time()-self.hold
			self.up = time()
			if 0.01 < self.last_hold < 0.3 and 0.01 <  self.last_up < 0.3 and 0.01 <  self.hold < 0.3:
				self.double_tap = True
				self.double_tap_time = time()
				self.hold = 0

		if time()-self.double_tap_time > 0.5:
			self.double_tap = False