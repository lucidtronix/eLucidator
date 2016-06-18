# ImageStreamDir.py
# Class for LucidTronix ImageStream objects loaded from Instagram API
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import urllib
import threading
import numpy as np
import urllib as ur
from PIL import Image
from io import BytesIO
import urllib, cStringIO
from ImageStream import ImageStream
from instagram.client import InstagramAPI
from io import BytesIO
from time import time, sleep  

from instagram.client import InstagramAPI

access_token ='585822756.695a083.0585d82aaee947edb21bfaf3cf4273de'

api = InstagramAPI(access_token=access_token,  
					client_ips="99.47.41.77",
					client_secret="23eae31d8de84810b9b1344c25ee3a6a")



class ImageStreamInstagram(ImageStream):
	def __init__(self, format='pygame', user='', tag='', cache_path='./'):
		super(ImageStreamInstagram, self).__init__('Instagram', format, cache_path)
		self.user = user
		self.tag = tag
		#self.api = self.get_instagram_api()
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
			#del self.image_buffer

		return super(ImageStreamInstagram, self).next()

	def start_query_thread(self):
		if self.user != '':
			self.iq = InstagramQuery(self.image_buffer, self.user, "user")
			self.iq.start()
			print ('Query Started in ImageStreamInstagram')		
		elif self.tag != '':
			self.iq = InstagramQuery(self.image_buffer, self.tag, "tag")
			self.iq.start()
			print ('Query Started in ImageStreamInstagram')		
		else:
			print ('Must specifiy user or tag in ImageStreamInstagram')				

	# def get_instagram_api(self):
	# 	access_token ='585822756.695a083.0585d82aaee947edb21bfaf3cf4273de'

	# 	return InstagramAPI(access_token=access_token,  
	# 				client_ips="99.47.41.77",
	# 				client_secret="23eae31d8de84810b9b1344c25ee3a6a")


class InstagramQuery(threading.Thread):
	def __init__(self, images, keyword, atype):
		super(InstagramQuery, self).__init__()
		self.images = images
		self.keyword = keyword
		self.atype = atype
		self.count = 3

	def run(self):

		new_images = []
		if self.atype == "tag":
			new_images = get_tag_images(self.keyword, self.count)
		elif self.atype == "user":
			new_images = get_user_images(self.keyword, self.count)

		if len(new_images) > 0:
			self.images += new_images
			print("Got:"+str(len(self.images))+" in Instagram query thread.")

		print("Query ended")


def get_tag_images(tag="magicegg", count=5):
	try:
		print("Load images from tag:" + tag)
		recent_media, url = api.tag_recent_media(tag_name=tag, count=count)
		new_images = []
		print("Loaded:"+str(len(recent_media))+" recent media from tag:" + tag)

		for media in recent_media:  
			# Where the media is
			id_ = media.id
			# List of users that like the image
			#users = [user.username for user in media.likes]

			if media.type == 'image':
				iimg = InstagramMedia(media, tag)
				new_images.append(iimg)
			sleep(1)
		print("Loaded:"+str(len(new_images))+" images from tag:" + tag)
		return new_images
	except:
		e = sys.exc_info()[0]
		print 'error in TAG instagram query:', e


def get_user_images(user_name, count=1):
	print('Loook for user:' + user_name)
	results = api.user_search(user_name, count=2)
	uid = results[0].id
	print 'Load images from user:' + user_name + ' user id:' + uid
	recent_media, url = api.user_recent_media(user_id=uid, count=count)
	new_images = []
	for media in recent_media:
		id_ = media.id
		if media.type == 'image':
			print("Image media images from user:" + user_name)
			iimg = InstagramMedia(media, user_name)
			print("Iimg" + iimg.get_file_name())
			new_images.append(iimg)
		sleep(1)
	print("Loaded:"+str(len(new_images))+" images from user:" + user_name)
	
	return new_images


class InstagramMedia:
	def __init__(self, media, source):
		self.media = media
		self.source = source
		if self.media.type == 'image':
			print 'Try to make inst media'

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
		#try:
		print("Try to load image:" + url)
		resp = ur.urlopen(url)
		self.pil_image = Image.open(BytesIO(resp.read()))

		# except Exception, e:
		# 	print "URL to image unexpected error:", str(e)
		# 	raise	

	def to_surface(self):
		mode = self.pil_image.mode
		size = self.pil_image.size
		data = self.pil_image.tostring()
		surface = pygame.image.fromstring(data, size, mode)
		return surface

