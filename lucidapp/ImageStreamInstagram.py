# ImageStreamDir.py
# Class for LucidTronix ImageStream objects loaded from Instagram API
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import defines
import threading
import numpy as np
import urllib as ur
from PIL import Image
from io import BytesIO
from time import time, sleep  
from ImageStream import ImageStream
from instagram.client import InstagramAPI




class ImageStreamInstagram(ImageStream):
	def __init__(self, user='', tag='', cache_path=defines.base_path+''):
		super(ImageStreamInstagram, self).__init__('Instagram', cache_path)
		self.user = user
		self.tag = tag
		self.api = self.get_instagram_api()
		self.image_buffer = []
		self.last_query = time()
		self.queried = False
	def __str__(self):
		return super(ImageStreamInstagram, self).__str__() + ", " +  self.dir_path

	def next(self):
		if time() -  self.last_query > 2.0 and not self.queried:
			self.last_query = time()
			self.start_query_thread()
			self.queried = True
		print 'image buffer is:', len(self.image_buffer)
		if len(self.image_buffer) > 0:
			print ('Image buffer sync in ImageStreamInstagram')

			super(ImageStreamInstagram, self).add_all(self.image_buffer)
			del self.image_buffer
			self.image_buffer = []

		return super(ImageStreamInstagram, self).next()

	def start_query_thread(self):
		if self.user != '':
			self.iq = InstagramQuery(self.api, self.image_buffer, self.user, "user")
			self.iq.start()
			print ('Query Started in ImageStreamInstagram')		
		elif self.tag != '':
			self.iq = InstagramQuery(self.api, self.image_buffer, self.tag, "tag")
			self.iq.start()
			print ('Query Started in ImageStreamInstagram')		
		else:
			print ('Must specifiy user or tag in ImageStreamInstagram')				

	def get_instagram_api(self):
		access_token ='585822756.695a083.0585d82aaee947edb21bfaf3cf4273de'

		return InstagramAPI(access_token=access_token,  
					client_ips="99.47.41.77",
					client_secret="23eae31d8de84810b9b1344c25ee3a6a")


class InstagramQuery(threading.Thread):
	def __init__(self, api, images, keyword, atype):
		super(InstagramQuery, self).__init__()
		self.api = api
		self.images = images
		self.keyword = keyword
		self.atype = atype
		self.count = 3

	def run(self):

		new_images = []
		if self.atype == "user":
			new_images = self.get_user_images(self.keyword)

		if len(new_images) > 0:
			self.images += new_images
			print("Got:"+str(len(self.images))+" in Instagram query thread.")

		print("Query ended")


	def get_user_images(self, user_name):
		results = self.api.user_search(user_name, count=2)
		uid = results[0].id
		print 'Load images from user:' + user_name + ' user id:' + uid
		recent_media, url = self.api.user_recent_media(user_id=uid, count=self.count)
		new_images = []
		for media in recent_media:
			id_ = media.id
			if media.type == 'image':
				iimg = InstagramMedia(media, user_name)
				new_images.append(iimg)
			sleep(0.5)
		print("Loaded:"+str(len(new_images))+" images from user:" + user_name)
		
		return new_images


class InstagramMedia:
	def __init__(self, media, source):
		self.media = media
		self.source = source
		if self.media.type == 'image':
			img_url = self.media.images['standard_resolution'].url
			img_file = self.get_file_name()
			self.url_to_image(img_url)

			# print('saving url:'+img_url+'to:'+img_file)
			# img_path = os.path.join(instagram_cache_path, source)
			# img_path_file = os.path.join(img_path,img_file)
			# if not os.path.exists(img_path):
			# 	os.makedirs(img_path)
			# elif os.path.exists(img_path_file):
			# 	print("Image already cached.")
			# else:
			# 	self.pil_image.save(img_path_file)
	
	def get_file_name(self):
		img_url = self.media.images['standard_resolution'].url
		img_file = img_url.replace("http://", "").replace("/", "__").strip()
		img_file = img_file.split('?', 1)[0]
		return img_file

	def url_to_image(self, url):
		print("Try to load image:" + url)
		resp = ur.urlopen(url)
		self.pil_image = Image.open(BytesIO(resp.read()))
