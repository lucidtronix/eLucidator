# ImageStreamDir.py
# Class for LucidTronix ImageStream objects loaded from Instagram API
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import pygame
import threading
import numpy as np
from PIL import Image
from io import BytesIO
import urllib, cStringIO
from ImageStream import ImageStream
from instagram.client import InstagramAPI

class ImageStreamInstagram(ImageStream):
	def __init__(self, format='pygame', user='', tag='', cache_path='./'):
		super(ImageStreamInstagram, self).__init__('Instagram', format, cache_path, None)
		self.user = user
		self.tag = tag
		self.api = self.get_instagram_api()
		self.image_buffer = {}

		if self.user != '':
			iq = InstagramQuery(self.image_buffer, self.user, "user", self.api)
			iq.start()
		elif self.tag != ''
			iq = InstagramQuery(self.image_buffer, self.tag, "tag", self.api)
			iq.start()
		else:
			print ('Must specifiy user or tag in ImageStreamInstagram')

	def __str__(self):
		return super(ImageStreamInstagram, self).__str__() + ", " +  self.dir_path

	def next(self):
		if len(self.image_buffer) > 0:
			super(ImageStreamInstagram, self).add_all(self.image_buffer)
			del self.image_buffer

		return super(ImageStreamInstagram, self).next()

	def get_instagram_api(self):
		access_token ='585822756.695a083.0585d82aaee947edb21bfaf3cf4273de'

		return InstagramAPI(access_token=access_token,  
					client_ips="99.47.41.77",
					client_secret="23eae31d8de84810b9b1344c25ee3a6a")


class InstagramQuery(threading.Thread):
	def __init__(self, images, keyword, atype, api):
		super(InstagramQuery, self).__init__()
		self.images = images
		self.keyword = keyword
		self.type = atype
		self.api = api
		self.count = 3

	def run(self):
		new_images = []
		if self.type == "tag":
			new_images = self.get_tag_images(self.keyword, self.count)
		elif self.type == "user":
			new_images = self.get_user_images(self.keyword, self.count)
		print("Got:"+str(len(new_images))+"in Instagram query thread.")

		if len(new_images) > 0:
			self.images += new_images

	def get_tag_images(self, tag="magicegg", count=5):
		print("Load images from tag:" + tag)
		recent_media, url = self.api.tag_recent_media(tag_name=tag, count=count)
		images = {}
		for media in recent_media:  
			# Where the media is
			id_ = media.id
			# List of users that like the image
			#users = [user.username for user in media.likes]

			if media.type == 'image':
				iimg = InstagramMedia(media, tag)
				images[iimg.get_file_name()] = iimg
		return images

	def get_user_images(self, user_name, count=5):
		results = self.api.user_search(user_name, count=1)
		uid = results[0].id
		print('Load images from user:' + user_name + ' user id:' + uid)
		recent_media, url = api.user_recent_media(user_id=uid, count=count)
	        
		imagimageses = []
		for media in recent_media:
	                # Where the media is
			id_ = media.id
	                # List of users that like the image
	                #users = [user.username for user in media.likes]
	                #print "Likers:", users[:8]
	                #print "Media type:", media.type
	                #print("Media tags:"+ str(media.tags))
	                #print("Media caption:"+ str(media.caption))
			if media.type == 'image':
				iimg = InstagramMedia(media, user_name)
				images[iimg.get_file_name()] = iimg
		return images

class InstagramMedia:
	def __init__(self, media, source):
		self.media = media
		if media.type == 'image':
			img_url = media.images['standard_resolution'].url
			img_file = self.get_file_name()
			self.pil_image = self.url_to_image(img_url)
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
		img_url = media.images['standard_resolution'].url
		img_file = img_url.replace("http://", "").replace("/", "__").strip()
		img_file = img_file.split('?', 1)[0]
		return img_file

	def url_to_image(self, url):
		print("Try to load image:" + url)
		resp = ur.urlopen(url)
		img = Image.open(BytesIO(resp.read()))
		# return the image
		print("Img size:"+str(img.size))
		return img	

def pil_image_to_surface(img):
	mode = img.mode
	size = img.size
	data = img.tostring()
	surface = pygame.image.fromstring(data, size, mode)
	return surface

