# ImageStream.py
# Base Class for LucidTronix ImageStream objects
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import defines
import numpy as np
from PIL import Image
import urllib, cStringIO
from threading import Thread

class ImageStream(object):
	def __init__(self, source='dir', cache_path=defines.base_path+''):
		super(ImageStream, self)
		self.source = source
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
		else:
			return InternetImage(cv_img=np.zeros(defines.image_crop))

	def next(self, crop=None):
		if len(self.images) > 0:
			image = self.images[self.cur_image]
			self.cur_image = (self.cur_image+1) % self.size()
			return image
		else:
			return InternetImage(cv_img=np.zeros(defines.image_crop))

	def size(self):
		return len(self.images)



class InternetImage(object):
	def __init__(self, img_path="", keyword_path="", crop=(400,300), cv_img=None):
		super(InternetImage, self)
		self.crop = crop
		self.img_path = img_path
		self.keyword_path = keyword_path
		self.cv_img = cv_img
		self.scale = 1.0
		
		if self.cv_img is None:
			self.loaded = False
			lt = Thread(target=self.load)
			lt.start()
		else:
			self.loaded = True

		self.error = False
		self.pil_img = None


	def load(self):
		if 'http' in self.img_path:
			self.load_image_url()
		else:
			self.load_image_file()

	def load_image_file(self):
		try:
			pic = cv2.imread(self.img_path)
			self.scale = self.crop[0] / float(pic.shape[1])
			dim = (self.crop[0], int(pic.shape[0] * self.scale))
			if dim[1] > self.crop[1]:
				self.scale  = self.crop[1] / float(pic.shape[0])
				dim = (int(pic.shape[1] * self.scale ), self.crop[1])
			
			self.cv_img = cv2.resize(pic, dim, interpolation=cv2.INTER_AREA)
			self.loaded = True
		except Exception, e:
			print 'Image from file Error reading:', self.img_path
			print 'Error message:', e.message
			self.error = True

	def load_image_url(self):
		try:
			print 'Try to load url image at:', self.img_path
			ifile = cStringIO.StringIO(urllib.urlopen(self.img_path).read())
			self.pil_img = Image.open(ifile).convert('RGB')
			self.scale = self.crop[0] / float(self.pil_img.size[0])
			dim = (self.crop[0], int(self.pil_img.size[1] * self.scale))
			if dim[1] > self.crop[1]:
				self.scale  = self.crop[1] / float(self.pil_img.size[1])
				dim = (int(self.pil_img.size[0] * self.scale ), self.crop[1])
			print 'Try to resize image from:', self.pil_img.size, 'to:', dim, 'crops ', self.crop, 'scale is', self.scale
			self.pil_img = self.pil_img.resize(dim, Image.ANTIALIAS)

			self.cv_img = np.array(self.pil_img)
			self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)

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


	def to_array(self):
		if self.loaded and self.cv_img is not None:
			return self.cv_img
		elif self.error:
			imge = cv2.imread(defines.base_path+'/images/cat.jpg')
			return cv2.resize(imge, self.crop, interpolation=cv2.INTER_AREA)
		else:
			imgl = cv2.imread(defines.base_path+'/images/dog.jpg')
			return cv2.resize(imgl, self.crop, interpolation=cv2.INTER_AREA)


	def get_size(self):
		return self.crop
