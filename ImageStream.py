# ImageStream.py
# Base Class for LucidTronix ImageStream objects
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import numpy as np
from PIL import Image
import urllib, cStringIO
from threading import Thread

class ImageStream(object):
	def __init__(self, source='dir', format='pygame', cache_path='./'):
		super(ImageStream, self)
		self.source = source
		self.format = format
		self.cache_path = cache_path
		self.recording = False
		self.images = []
		self.cur_image = 0

	def __str__(self):
		return "Image Stream from:" +  self.source


	def prev(self, crop=None):
		if len(self.images) > 0:
			self.cur_image = (self.cur_image-1) % self.size()
			return  self.images[self.cur_image]
		elif self.format == 'pygame':
			print 'returning dog as pygame'
			return InternetImage('./images/dog.jpg', './images/')
		else:
			print 'next failed returning None.', self.format
			return None

	def next(self, crop=None):
		if len(self.images) > 0:
			image = self.images[self.cur_image]
			self.cur_image = (self.cur_image+1) % self.size()
			return image
		elif self.format == 'pygame':
			print 'returning dog as pygame'
			return InternetImage('./images/dog.jpg', './images/')
		else:
			print 'next failed returning None.', self.format
			return None

	def size(self):
		return len(self.images)



class InternetImage:
	def __init__(self, img_path, keyword_path, format='cv2'):
		self.crop = (400, 300)
		self.img_path = img_path
		self.keyword_path = keyword_path
		self.format = format
		self.loaded = False
		self.error = False
		self.pil_img = None
		self.cv_img = None

		lt = Thread(target=self.load)
		lt.start()

	def load_image_file(self):
		try:
			if self.format == 'pygame':
				print 'Loading image from file:', self.img_path
				self.pil_img = Image.open(self.img_path).convert('RGB')
				self.pil_img = self.pil_img.resize(self.crop, Image.ANTIALIAS)
				self.loaded = True
			elif self.format == 'cv2':
				pic = cv2.imread(self.img_path)
				self.cv_img = cv2.resize(pic, self.crop, interpolation = cv2.INTER_AREA)
				self.loaded = True
		except Exception, e:
			print 'Image from file Error reading:', self.img_path
			print 'Error message:', e.message
			self.error = True

	def load_image_url(self):
		try:
			print 'Try to load url image at:', self.img_path
			ifile = cStringIO.StringIO(urllib.urlopen(self.img_path).read())
			print 'Try to OPEN url image.'
			self.pil_img = Image.open(ifile).convert('RGB')
			print 'Try to RESIZE url image.'
			self.pil_img = self.pil_img.resize(self.crop, Image.ANTIALIAS)

			if 'cv2' == self.format:
				self.cv_img = np.array(self.pil_img)

			self.img_path = os.path.join(self.keyword_path, os.path.basename(self.img_path))
			if not os.path.exists(self.img_path):
				print 'Try to save image at:', self.img_path
				self.pil_img.save(self.img_path)
				print 'Saved image at:', self.img_path

			self.loaded = True	

		except Exception, e:
			print 'Error loading image from URL:', self.img_path
			print 'Error message:', e.message
			self.error = True

	def load(self):
		if 'http' in self.img_path:
			self.load_image_url()
		else:
			self.load_image_file()

	def to_surface(self):
		if self.loaded and self.pil_img:
			mode = self.pil_img.mode
			size = self.pil_img.size
			data = self.pil_img.tostring()
			surface = pygame.image.fromstring(data, size, mode)
			return surface
		elif self.error:
			return pygame.image.load('./images/cat.jpg')
		else:
			return pygame.image.load('./images/dog.jpg')

	def to_array(self):
		if self.loaded and self.cv_img is not None:
			return self.cv_img
		elif self.error:
			imge = cv2.imread('./images/cat.jpg')
			return cv2.resize(imge, self.crop, interpolation=cv2.INTER_AREA)
		else:
			imgl = cv2.imread('./images/dog.jpg')
			return cv2.resize(imgl, self.crop, interpolation=cv2.INTER_AREA)


	def get_size(self):
		return self.crop
