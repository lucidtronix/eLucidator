# ImageStreamDir.py
# Class for LucidTronix ImageStream objects loaded from an existing directory
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
from ImageStream import ImageStream, InternetImage

class ImageStreamDir(ImageStream):
	def __init__(self, load_strategy='all', format='pygame', dir_path='./images/'):
		super(ImageStreamDir, self).__init__('dir', format, None)
		self.dir_path = dir_path
		self.load_strategy = load_strategy
		if 'all' == self.load_strategy:
			self.load_all()

	def __str__(self):
		return super(ImageStreamDir, self).__str__() + ", " +  self.dir_path

	def next(self):
		return super(ImageStreamDir, self).next()

	def load_all(self):
		if "pygame" == self.format:
			imgs = os.listdir(self.dir_path)
			for img_id in imgs:
				#img = pygame.image.load(self.dir_path+img_id)
				ii = InternetImage(self.dir_path+img_id, self.dir_path)
				ii.load()
				self.images.append(ii)
			print 'Loaded'+str(len(self.images))+'Images pygame style.'

