# ImageStreamLink.py
# Class for LucidTronix ImageStream objects loaded from an existing directory
# Samwell Freeman
# September 2016

import os
import re
import sys
import cv2
import pygame
import defines
import urllib2
import threading
import feedparser
import numpy as np
from PIL import Image
import urllib, cStringIO
from bs4 import BeautifulSoup
from cookielib import CookieJar
from ImageStream import ImageStream, InternetImage

imageTypes = ['.jpg', '.jpeg', '.png']

class ImageStreamLink(ImageStream):
	def __init__(self, url, keyword, format='cv2'):
		super(ImageStreamLink, self).__init__('link', format, None)
		self.url = url 
		self.keyword = keyword

		self.img_links = []
		self.get_image_links()

		self.loaded = [False for _ in self.img_links]

		self.keyword_path =defines.base_path+'cache/link/' + self.keyword
		if not os.path.exists(self.keyword_path):
			os.makedirs(self.keyword_path)

	def get_image_links(self):
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		p = opener.open(self.url)

		page = BeautifulSoup(p)
		img_tags = page.findAll('img')
		print "Found:", len(img_tags), "images at page:", self.url

		for img in img_tags:
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(img))
			for img_link in urls:
				self.img_links.append(img_link)

	def __str__(self):
		return "ImageStreamLink " +  self.keyword_path

	def next(self):
		if self.loaded[self.cur_image]:
			return self.images[self.cur_image]
		if not self.loaded[self.cur_image]:
			ii = InternetImage(self.img_links[self.cur_image], self.keyword_path)
			ii.load()
			self.loaded[self.cur_image] = True
			self.cur_image = (self.cur_image+1) % len(self.img_links)
			if self.size() < len(self.img_links):
				self.images.append(ii)
			return ii

	def size(self):
		return len(self.img_links)