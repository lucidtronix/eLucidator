# TouchScreen.py
# TouchScreen for LucidTronix eLucidator
# Samwell Freeman
# June 2016

import cv2
import math
import pygame
from time import time

class TouchScreen:
	def __init__(self):
		self.start = (0,0)
		self.delta = (0,0)
		self.ease = (0.0,0.0)
		self.ease_start = (0.0,0.0)
		self.ease_scale = 0.001
		self.last_hold = 0
		self.last_up = 0
		self.up = 0
		self.hold = 0
		self.sliding = False
		self.easing = False
		self.double_tap = False
		self.double_tap_time = 0
		self.base_graphics = 'cv2'
		self.mx = 0
		self.my = 0
		self.b1 = False
		if self.base_graphics == 'cv2':
			mouse_params = [self]
			cv2.setMouseCallback('canvas', mouse_callback_cv, mouse_params)

	def update(self):
		if self.base_graphics == 'pygame':
			mx, my = pygame.mouse.get_pos()
			b1, b2, b3 = pygame.mouse.get_pressed()
		elif self.base_graphics == 'cv2':
			mx = self.mx
			my = self.my
			b1 = self.b1
		if b1:
			self.double_tap = False
			if not self.sliding:
				self.last_up = time()- self.up
				self.last_hold = self.hold
				self.hold = time()
				self.sliding = True
				self.easing = False
				self.start = (mx, my)
			self.delta = (mx - self.start[0], my - self.start[1])
		elif self.sliding:
			self.sliding = False
			self.hold = time()-self.hold
			self.up = time()
			self.easing = True
			self.ease = self.delta
			self.ease_start = (self.ease_scale*float(self.delta[0])/self.hold, self.ease_scale*float(self.delta[1])/self.hold)
			if 0.01 < self.last_hold < 0.3 and 0.01 <  self.last_up < 0.3 and 0.01 <  self.hold < 0.3:
				self.double_tap = True
				self.double_tap_time = time()
				self.hold = 0
		if self.easing:
			ease_t = time() - self.up
			self.ease = (self.ease[0] + (self.ease_start[0]*math.exp(-ease_t)), self.ease[1] + (self.ease_start[1]*math.exp(-ease_t)))
			self.delta = (int(self.ease[0]), int(self.ease[1]))
			if ease_t > 3.5:
				self.easing = False
		if time()-self.double_tap_time > 0.5:
			self.double_tap = False

# mouse callback function
def mouse_callback_cv(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		param[0].b1 = True
	elif event == cv2.EVENT_LBUTTONUP:
		param[0].b1 = False
	elif event == cv2.EVENT_RBUTTONDBLCLK:
		print 'R dubble click'
	elif event == cv2.EVENT_MOUSEMOVE:	
		param[0].mx = x
		param[0].my = y


def sigmoid(x):
  return 1 / (1 + math.exp(-x))