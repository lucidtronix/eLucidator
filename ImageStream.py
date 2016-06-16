# ImageStream.py
# Base Class for LucidTronix ImageStream objects
# Samwell Freeman
# June 2016

import os
import sys
import cv2
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
		new_ids = new_images.keys()
		self.images.update(new_images)
		for iid in new_ids:
			self.loaded[image_id] = True
			self.order.append(image_id)	

	def next(self, crop=None):
		if len(self.images) > 0:
			image = self.images[self.order[self.cur_order]]

			self.cur_order += 1
			if self.cur_order == len(self.order):
				self.cur_order = 0
		
			return image
		elif self.format == 'pygame':
			pygame.image.load('./images/dog.jpg')



