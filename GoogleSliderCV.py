# LucidApp.py
# Base Class for LucidTronix eLucidator Applications
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
from ImageStreamGoogle import ImageStreamGoogle

class GoogleSlider(LucidApp):
	def __init__(self, cache_path='./cache/', fullscreen=False, resolution=(500, 400), icon=None, base_graphics='cv2'):
		super(GoogleSlider, self).__init__('GoogleSlider', cache_path, fullscreen, resolution, icon, base_graphics)
		self.playing = True
		self.ts = TouchScreen()
		self.buttons.append(Button(self, 'more', (75,10,65,30), (25,250,250), self.get_more_images))
		self.keywords = ['fractals', 'lucidtronix', 'trending', 'beauty', 'sunset', 'caravaggio', 'chiaroscuro', 
						'evolution', 'ocean', 'samwell freeman', 'neural network', 'achievement', 'trees', 'palms',
						'friends', 'cute animals', 'learning', 'truth', 'current events', 'news', 'timeless', 'mountains']
		self.cur_keyword = random.randrange(len(self.keywords))
		self.stream = ImageStreamGoogle((480, 640, 3), "google", cache_path, 'pygame', self.keywords[self.cur_keyword], 5, 0)
		self.row = ImageRow(self, self.stream, self.ts, self.resolution)
		self.redraw = True
		self.search_string = ""
	def __str__(self):
		return super(ImageSlider, self).__str__() + 'Playing:' + str(self.playing)

	def open(self):
		pass

	def close(self):
		pass

	def handle_keys(self):
		if self.base_graphics == 'pygame':
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					return -1
				elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return -1
		elif self.base_graphics == 'cv2':
			char = cv2.waitKey(1) & 0xFF
			if char > 31 and char < 127:
				self.search_string += str(chr(char))

			elif char == 27: # Escape
				cv2.destroyAllWindows()
				return -1
			elif char == 8: # Delete
				if len(self.search_string):
					self.search_string = self.search_string[:-1]
			elif char == 10: # Enter/return key
				if len(search_string):
					self.stream.add_keyword(self.keywords[self.cur_keyword])
					self.stream.start_query()
			elif char == 9: # Tab
				print 'tab'
			elif char == 226: # Right shift
				print 'right shift'

			elif char == 227: # Left Ctrl
				print 'left ctrl'
			elif char == 228: # Right Ctrl
				print 'right ctrl'
			elif char != 255:
				print 'special char:', char
		return 0

	def run(self):
		cx = oldx = 0
		pic_update = 0
		cur_img = self.stream.next()
		quit = False
		while not quit:
			self.ts.update()
			self.row.update()
			self.row.display()

			if self.redraw or self.row.redraw:
				self.label(self.keywords[self.cur_keyword], 300, 12)
				self.draw()

			ret = self.handle_keys()
			if ret < 0:
				quit = True

			for b in self.buttons:
				b.show()
				if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press()
					if ret < 0:
						quit = True

					self.ts.double_tap = False

	def get_more_images(self):
		self.cur_keyword = (self.cur_keyword+1)%len(self.keywords)
		self.stream.add_keyword(self.keywords[self.cur_keyword])
		self.stream.start_query()
		
		self.fill()
		self.redraw = True
		self.row.redraw = True


class ImageRow:
	def __init__(self, parent, stream, ts, resolution, wrap=True):
		self.parent = parent
		self.stream = stream
		self.ts = ts
		self.resolution = resolution
		self.wrap = wrap
		self.margin = 10
		self.corner = (self.margin, 5*self.margin)
		self.last_corner = (self.margin, 5*self.margin)
		self.images = []
		self.redraw = False
		self.cur_image = 1


	def update(self):
		if len(self.images) > 2:
			
			if self.ts.sliding:
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

	def next_index(self):
		return (self.cur_image+1) % len(self.images)

	def display_pygame(self):
		pass
		# if self.redraw and len(self.images) > 2:
		# 	self.surface.fill(0)
		# 	self.surface.blit(self.images[self.cur_image].to_surface(), self.corner)
		# 	if self.corner[0] < 0:
		# 		size = self.images[self.cur_image].to_surface().get_size()
		# 		rp = (self.corner[0] + size[0] + self.margin, self.corner[1])
		# 		self.surface.blit(self.images[self.next_index()].to_surface(), rp)
		# 	else:
		# 		size = self.images[self.prev_index()].get_size()
		# 		lp = (self.corner[0] - (size[0]+self.margin), self.corner[1])
		# 		self.surface.blit(self.images[self.prev_index()].to_surface(), lp)			

	def display(self):
		if self.redraw and len(self.images) > 2:
			self.parent.fill()
			self.parent.show_image(self.images[self.cur_image], self.corner)
			if self.corner[0] < 0:
				size = self.images[self.cur_image].to_surface().get_size()
				rp = (self.corner[0] + size[0] + self.margin, self.corner[1])
				self.parent.show_image(self.images[self.next_index()], rp)
			else:
				size = self.images[self.prev_index()].get_size()
				lp = (self.corner[0] - (size[0]+self.margin), self.corner[1])
				self.parent.show_image(self.images[self.prev_index()], lp)	




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	app = GoogleSlider(fullscreen=args.fullscreen)
	app.run()