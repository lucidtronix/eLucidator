# ImageRow.py
# ImageRow for LucidTronix eLucidator Applications
# A row of images loaded from an ImageStream that support basic touch screen interactions
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import random
import argparse
import threading
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from TouchScreen import TouchScreen
from LucidApp import LucidApp, Button
from ImageStreamDir import ImageStreamDir

class ImageRow:
	def __init__(self, parent, stream, ts, resolution, wrap=True):
		self.parent = parent
		self.stream = stream
		self.ts = ts
		self.resolution = resolution
		self.wrap = wrap
		self.margin = 10
		self.corner = (self.margin, 7*self.margin)
		self.last_corner = (self.margin, 7*self.margin)
		self.images = []
		self.redraw = False
		self.cur_image = 1
		self.was_easing = False

		self.images.append(self.stream.next())
		self.images.append(self.stream.next())
		
	def update(self):
		if len(self.images) > 2:
			
			if self.ts.sliding or self.ts.easing:
				if self.was_easing and self.ts.sliding:
					self.last_corner = self.corner
				self.corner = (self.last_corner[0] + self.ts.delta[0], self.corner[1])
				self.redraw = True
				if self.corner[0] + self.image_widths() < self.resolution[0]:
					self.cur_image = (self.cur_image+1)%len(self.images)
					self.corner = (self.margin, self.corner[1])
					self.last_corner = (self.last_corner[0] + self.images[self.prev_index()].get_size()[0], self.corner[1])
				elif self.corner[0] > self.images[self.cur_image].get_size()[0]+self.margin:
					self.corner = (self.corner[0]-self.images[self.cur_image].get_size()[0], self.corner[1])
					self.last_corner = (self.last_corner[0] -self.images[self.cur_image].get_size()[0], self.corner[1])
					self.cur_image = (self.cur_image-1)%len(self.images)
			else:
				self.last_corner = self.corner
				self.redraw = False

			if self.ts.easing:
				self.was_easing = True
			else:
				self.was_easing = False

			if self.images[self.next_index()].error:
				del self.images[self.next_index()]

		if self.stream.size() > len(self.images):
			self.images.append(self.stream.next())
			print ' Adding image from stream...',  self.images[len(self.images)-1].img_path


	def image_widths(self):
		if self.corner[0] < 0:
			return self.images[self.cur_image].get_size()[0] + self.images[self.next_index()].get_size()[0] + (2*self.margin)
		else:
			return self.images[self.cur_image].get_size()[0] + self.images[self.prev_index()].get_size()[0] + (2*self.margin)


	def prev_index(self):
		return (self.cur_image-1) % len(self.images)

	def prev_prev_index(self):
		return (self.cur_image-2) % len(self.images)

	def next_index(self):
		return (self.cur_image+1) % len(self.images)		

	def next_next_index(self):
		return (self.cur_image+2) % len(self.images)

	def display(self):
		if len(self.images) > 2:
			self.parent.fill()
			self.parent.show_image(self.images[self.cur_image], self.corner)
			c_img_x = self.images[self.cur_image].get_size()[0]
			rp = (self.corner[0] + c_img_x +self.margin, self.corner[1])
			lp = (self.corner[0] - (self.images[self.prev_index()].get_size()[0]+self.margin), self.corner[1])
			if self.corner[0] < 0:
				self.parent.show_image(self.images[self.next_index()], rp)
				if self.corner[0] > self.margin:
					self.parent.show_image(self.images[self.prev_index()], lp)
			else:
				self.parent.show_image(self.images[self.prev_index()], lp)	
				if rp[0] < self.resolution[0]:
					self.parent.show_image(self.images[self.next_index()], rp)


