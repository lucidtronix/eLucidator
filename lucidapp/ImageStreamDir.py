# ImageStreamDir.py
# Class for LucidTronix ImageStream objects loaded from an existing directory
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import defines
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO
from ImageStream import ImageStream, InternetImage

imageTypes = ['.jpg', '.jpeg', '.png']

class ImageStreamDir(ImageStream):
	def __init__(self, load_strategy='paths', dir_path=defines.base_path+'/images/'):
		super(ImageStreamDir, self).__init__('dir', None)
		self.dir_path = dir_path
		self.load_strategy = load_strategy
		
		if 'all' == self.load_strategy:
			self.load_all()
		elif 'paths' == self.load_strategy:
			self.image_paths = self.get_paths(self.dir_path, imageTypes)
			print 'got:', len(self.image_paths), 'image paths.'
			if not len(self.image_paths) > 0:
				raise ValueError('No images found in:'+self.dir_path)
			self.img_idx = 0


	def __str__(self):
		return super(ImageStreamDir, self).__str__() + ", " +  self.dir_path

	def next(self):
		if 'all' == self.load_strategy:
			return super(ImageStreamDir, self).next()
		else:
			ii = InternetImage(self.image_paths[self.img_idx], self.dir_path)
			ii.load()
			self.img_idx = (self.img_idx+1) % len(self.image_paths)
			if self.size() < len(self.image_paths):
				self.images.append(ii)
			return ii 

	def load_all(self):
		imgs = os.listdir(self.dir_path)
		for img_id in imgs:
			ii = InternetImage(self.dir_path+img_id, self.dir_path)
			ii.load()
			self.images.append(ii)
		print 'Loaded:' + str(len(self.images)) + ' InternetImages style.'


	def get_paths(self, path, fileTypes, recursive=True):
		## Returns list containing paths of files in /path/ that are of a file type in /fileTypes/,
		##      if /recursive/ is False subdirectories are not checked.
		paths = []
		if recursive:
			for root, folders, files in os.walk(path, followlinks=True):
				for file in files:
					for fileType in fileTypes:
						if file.endswith(fileType):
							paths.append(os.path.join(root, file))
		else:
			for item in os.listdir(path):
				for fileType in fileTypes:
					if item.endswith(fileType):
						paths.append(os.path.join(root, item))
		return paths
