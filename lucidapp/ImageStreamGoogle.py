# ImageStreamGoogle.py
# Written by Samwell Freeman
# November 2015

import os
import sys
import cv2
import defines
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from threading import Thread
from apiclient.discovery import build
from ImageStream import ImageStream, InternetImage


class ImageStreamGoogle(ImageStream):
	def __init__(self, shape, source, cache_path=defines.base_path+'cache/', keyword='fractal', num_images=3, search_offset=0, force_save=False):
		super(ImageStreamGoogle, self).__init__('google', cache_path=cache_path)
		self.shape = shape
		self.cache_path = cache_path

		self.image_search_start = search_offset
		self.num_images = num_images
		self.developer_key = 'AIzaSyCl7ZHvUAhfJQ8UNdpaR4Hpad02PZwZq0U'
		self.cx = "015656058763772975689:ovnlv9iv52u"
		
		self.keywords = [keyword]
		self.cur_keyword = 0
		self.query_wait = 2 # seconds
		self.last_query = time()#-self.query_wait
		self.start_query()

	def add_keyword(self, keyword):
		self.keywords.append(keyword)
		self.cur_keyword = (self.cur_keyword+1)%len(self.keywords)

	def start_query(self):
		if time() - self.last_query > self.query_wait:
			print 'Starting google image query for keyword:', self.keywords[self.cur_keyword]
			self.google_query(self.keywords[self.cur_keyword])
		else:
			print 'Query denied. Last query:', self.last_query

	def google_query(self, keyword):
		try:
			results = self.google_get_image_results(keyword)
			if not results:
				print 'Google image results:None for keyword:', keyword
				return
			print 'Got search results:', len(results)
			for item in results:
				keyword_path = os.path.join(self.cache_path, keyword)
				img_path =  os.path.join(keyword_path, os.path.basename(item['link']))
				if os.path.exists(img_path):
					print 'Try to make internet image keyword_path:',keyword_path
					ii = InternetImage(img_path, keyword_path)
				else:
					if not os.path.exists(keyword_path):
						os.makedirs(keyword_path)
					qindex = item['link'].find('?')
					if qindex != -1:
						print 'Got a Q:', item['link']
						item['link'] = item['link'][:qindex]
					print 'Title:', item['title'], 'Link:', item['link']
					ii = InternetImage(item['link'], keyword_path)

				self.images.append(ii)
			print 'Completed google image query for keyword:', keyword

		except Exception, e:
			print 'Error loading google image search results for keyword:', keyword
			print 'Error message:', e.message
			raise

	def google_get_image_results(self, keyword):
		try:
			service = build("customsearch", "v1", developerKey=self.developer_key)
			res = service.cse().list(
				q=keyword,
				cx=self.cx,
				searchType='image',
				num=self.num_images,
				imgType='clipart',
				fileType='jpg',
				safe= 'off'
			).execute()

			if not 'items' in res:
				print 'No result !'
				return None
			return res['items']
	
		except Exception, e:
			print 'Error executing google search for keyword:', keyword
			print 'Error message:', e
			return None

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