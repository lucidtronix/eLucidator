# ImageStream.py
# Base Class for LucidTronix ImageStream objects
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO

class ImageStream(object):
	def __init__(self, source='dir', format='pygame', cache_path='./'):
		super(ImageStream, self)
		self.source = source
		self.format = format
		self.cache_path = cache_path
		self.recording = False
		self.cur_image_id = ''
		self.cur_order = 0
		self.cached = {}
		self.loaded = {}
		self.images = {}
		self.order = []

	def __str__(self):
		return "Image Stream from:" +  self.source

	def add_image(self, image_id, image):
		self.images[image_id] = image
		self.loaded[image_id] = True
		self.order.append(image_id)

	def add_all(self, new_images):
		# new_ids = new_images.keys()
		# self.images.update(new_images)
		# for iid in new_ids:
		# 	self.loaded[image_id] = True
		# 	self.order.append(image_id)	
		for img in new_images:
			self.images[img.get_file_name()] = img.to_surface()
			self.loaded[img.get_file_name()] = True
			self.order.append(img.get_file_name())


	def next(self, crop=None):
		if len(self.images) > 0:
			image = self.images[self.order[self.cur_order]]

			self.cur_order += 1
			if self.cur_order == len(self.order):
				self.cur_order = 0
		
			return image
		elif self.format == 'pygame':
			print 'returning dog as pygame'
			return pygame.image.load('./images/dog.jpg')
		else:
			print 'next failed returning None.', self.format
			return None


	def to_surface(self, pil_image):
		mode = pil_image.mode
		size = pil_image.size
		data = pil_image.tostring()
		surface = pygame.image.fromstring(data, size, mode)
		return surface

