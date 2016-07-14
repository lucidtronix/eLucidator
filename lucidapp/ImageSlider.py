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
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class ImageSlider(LucidApp):
	def __init__(self, ts, cache_path='./cache/', fullscreen=False, resolution=(800, 400), 
					icon_path='./icons/image_slider.png', base_graphics='cv2'):
		super(ImageSlider, self).__init__('ImageSlider', cache_path, fullscreen, resolution, icon_path, base_graphics)
		self.playing = True
		#self.stream = ImageStreamGoogle((480, 640, 3), "google", cache_path, 'pygame', 'fractals', 5, 0)#ImageStreamDir()
		self.stream = ImageStreamDir()
		self.ts = ts
		self.row = ImageRow(self, self.stream, self.ts, self.resolution)
		#self.buttons.append()
	def __str__(self):
		return 'ImageSlider'

	def open(self):
		pass

	def close(self):
		pass

	def run(self):
		cx = oldx = 0
		pic_update = 0
		cur_img = self.stream.next()

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



if __name__ == '__main__':
	app = ImageSlider()
	app.run()