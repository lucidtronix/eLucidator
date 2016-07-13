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
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir
from ImageStreamGoogle import ImageStreamGoogle

class ImageSliderGrid(LucidApp):
	def __init__(self, cache_path='./cache/', fullscreen=False, resolution=(500, 400), 
					icon_path='./icons/image_slider.png', base_graphics='pygame'):
		super(ImageSliderGrid, self).__init__('ImageSliderGrid', cache_path, fullscreen, resolution, icon_path, base_graphics)
		self.playing = True
		#self.stream = ImageStreamGoogle((480, 640, 3), "google", cache_path, 'pygame', 'fractals', 5, 0)#ImageStreamDir()
		self.stream = ImageStreamDir()
		self.ts = TouchScreen()
		self.rows = []
		self.rows.append(ImageRow(self.stream, self.ts, self.surface, self.resolution, (10, 50)))
		self.rows.append(ImageRow(self.stream, self.ts, self.surface, self.resolution, (15, 370)))

		#self.buttons.append()
	def __str__(self):
		return super(ImageSliderGrid, self).__str__() + 'Playing:' + str(self.playing)

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

			update = False
			for r in self.rows:
				r.update()
				if r.redraw and not update:
					self.surface.fill(0)
					update = True
				r.display()
			if update:
				pygame.display.update()

			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					return 0
				elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return 0


			for b in self.buttons:
				mx, my = pygame.mouse.get_pos()
				b.show()
				if b.over(mx, my) and self.ts.double_tap and time()-b.last_press > 0.5:
					if b.press() < 0:
						return
					self.ts.double_tap = False



class ImageRow:
	def __init__(self, stream, ts, surface, resolution, corner, wrap=True):
		self.stream = stream
		self.ts = ts
		self.surface = surface
		self.resolution = resolution
		self.wrap = wrap
		self.margin = corner[0]
		self.corner = corner
		self.last_corner = (self.margin, self.corner[1])
		self.images = []
		self.redraw = False
		self.cur_image = 1



	def update(self):
		if len(self.images) > 2:
			if self.ts.sliding:
				self.corner = (self.last_corner[0]+self.ts.delta[0], self.last_corner[1]+self.ts.delta[1])
				self.redraw = True
				if self.corner[0] + self.image_widths() < self.resolution[0]:
					self.cur_image = (self.cur_image+1)%self.stream.size()
					self.corner = (self.margin, self.corner[1])
					self.last_corner = (self.last_corner[0] + self.images[self.prev_index()].get_size()[0], self.corner[1])
				elif self.corner[0] > self.images[self.cur_image].get_size()[0]+self.margin:
					self.corner = (self.corner[0]-self.images[self.cur_image].get_size()[0], self.corner[1])
					self.last_corner = (self.last_corner[0] -self.images[self.cur_image].get_size()[0], self.corner[1])
					self.cur_image = (self.cur_image-1)%self.stream.size()
			else:
				self.last_corner = self.corner
				self.redraw = False
		elif self.stream.size() > 2:
			print ' Adding images from stream...'
			for img in self.stream.images:
				self.images.append(img.to_surface())


	def image_widths(self):
		if self.corner[0] < 0:
			return self.images[self.cur_image].get_size()[0] + self.images[self.next_index()].get_size()[0] + (2*self.margin)
		else:
			return self.images[self.cur_image].get_size()[0] + self.images[self.prev_index()].get_size()[0] + (2*self.margin)



	def prev_index(self):
		return (self.cur_image-1) % self.stream.size()

	def next_index(self):
		return (self.cur_image+1) % self.stream.size()

	def display(self):
		if self.redraw and len(self.images) > 2:
			self.surface.blit(self.images[self.cur_image], self.corner)
			if self.corner[0] < 0:
				size = self.images[self.cur_image].get_size()
				rp = (self.corner[0] + size[0] + self.margin, self.corner[1])
				self.surface.blit(self.images[self.next_index()], rp)
			else:
				size = self.images[self.prev_index()].get_size()
				lp = (self.corner[0] - (size[0]+self.margin), self.corner[1])
				self.surface.blit(self.images[self.prev_index()], lp)			


if __name__ == '__main__':
	app = ImageSliderGrid()
	app.run()