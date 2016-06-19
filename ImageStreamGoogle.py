# google_image_search_api.py
# Written by Samwell Freeman
# November 2015

import os
import sys
import cv2
import pygame
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO
from apiclient.discovery import build
from ImageStream import ImageStream, InternetImage


class ImageStreamGoogle(ImageStream):
	def __init__(self, shape, source, cache_path='./cache/', format='pygame', keyword='fractal', num_images=10, search_offset=0, force_save=False):
		super(ImageStreamGoogle, self).__init__('google', format=format, cache_path=cache_path)
		self.shape = shape
		self.keyword = keyword
		self.cache_path = cache_path
		self.image_index = 0
		self.image_search_start = search_offset


		gq = GoogleQuery(self.images, self.keyword, self.cache_path, self.image_search_start)
		gq.start()


	def next(self):
		if self.image_index >= 0 and self.image_index < len(self.images):
			print 'Try to load image:', self.images[self.image_index].img_path
			if not self.images[self.image_index].loaded:
				self.images[self.image_index].load()
				if not self.images[self.image_index].loaded:
					self.image_index = (self.image_index+1) % len(self.images)
					# return np.zeros(self.shape, np.uint8)
				return super(ImageStreamGoogle, self).next()
			if self.images[self.image_index].img:
				self.image_index = (self.image_index+1) % len(self.images)
				return self.to_surface(self.images[self.image_index].img)

			else:
				print 'Could not load image:', self.images[self.image_index].img_path
				self.image_index = (self.image_index+1) % len(self.images)
				return np.zeros(self.shape, np.uint8)
		else:
			return super(ImageStreamGoogle, self).next()

	def completed_loop(self):
		return self.image_index == len(self.images)-1


class GoogleQuery(threading.Thread):
	def __init__(self, images, keyword, cache_path, image_search_start):
		super(GoogleQuery, self).__init__()
		self.images = images
		self.keyword = keyword
		self.cache_path = cache_path
		self.image_search_start = image_search_start
		self.developer_key = "AIzaSyCl7ZHvUAhfJQ8UNdpaR4Hpad02PZwZq0U"
		self.cx = "015656058763772975689:ovnlv9iv52u"
	def run(self):
		try:
			self.image_results = self.google_get_image_results(5)
			for item in self.image_results:
				keyword_path = self.cache_path + self.keyword + '/'
				img_path = keyword_path + os.path.basename(item['link'])
				if os.path.exists(img_path):
					ii = InternetImage(img_path, keyword_path)
				else:
					if not os.path.exists(keyword_path):
						os.makedirs(keyword_path)
					qindex = item['link'].find('?')
					if qindex != -1:
						print 'Got a Q:', item['link']
						item['link'] = item['link'][:qindex]
					print 'Title:', item['title'], 'Link:', item['link']
					ii = InternetImage(item['link'], keyword_path, url=True)

				ii.load()
				self.images.append(ii)


		except Exception, e:
			print 'Error loading google image search results for keyword:', self.keyword
			print 'Error message:', e.message
			raise


	def google_get_image_results(self, num_images):
		service = build("customsearch", "v1", developerKey=self.developer_key)
		print "Try to search"
		try:
			res = service.cse().list(
				q=self.keyword,
				cx=self.cx,
				searchType='image',
				num=num_images,
				imgType='clipart',
				fileType='png',
				safe= 'off'
			).execute()

			print "executed search", self.image_search_start
		except Exception, e:
			print 'Error executing search results for keyword:', self.keyword
			print 'Error message:', e
			return None
		# if not 'items' in res:
		# 	print 'No result !'
		# 	return None

		return res['items']

	def google_get_image(self, num_images):
		service = build("customsearch", "v1", developerKey=self.developer_key)

		res = service.cse().list(
			q=self.keyword,
			cx=self.cx,
			searchType='image',
			num=num_images,
			imgType='clipart',
			fileType='jpg',
			safe= 'off'
		).execute()

		if not 'items' in res:
			print 'No result !'
			return None

		for item in res['items']:
			print 'Title:', item['title'], 'Link:', item['link']
			try:
				ifile = cStringIO.StringIO(urllib.urlopen(item['link']).read())
				img = Image.open(ifile)
				keyword_path = self.cache_path + self.keyword + '/'
				img_path = keyword_path + os.path.basename(item['link'])
				if not os.path.exists(img_path):
					img.save(img_path)
					print 'Saved image at:', img_path
			except:
				print 'Error reading:', item['link']



if __name__ == '__main__':
	service = build("customsearch", "v1", developerKey="AIzaSyCl7ZHvUAhfJQ8UNdpaR4Hpad02PZwZq0U")

	res = service.cse().list(
		q='butterfly',
		cx='015656058763772975689:ovnlv9iv52u',
		searchType='image',
		num=1,
		imgType='clipart',
		fileType='png',
		safe= 'off'
	).execute()
	if not 'items' in res:
		print 'No result !!\nres is: {}'.format(res)
	else:
		for item in res['items']:
			print(item['title'], item['link'])