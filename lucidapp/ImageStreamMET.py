# ImageStreamMET.py
# Written by Samwell Freeman
# October 2016

import os
import re
import sys
import cv2
import random
import numpy as np
from time import time, sleep
from PIL import Image
import urllib2, cStringIO
from threading import Thread
from bs4 import BeautifulSoup
from cookielib import CookieJar
from ImageStream import ImageStream, InternetImage


class ImageStreamMET(ImageStream):
	def __init__(self, cache_path='./cache/met/', format='cv2'):
		super(ImageStreamMET, self).__init__('MET', format=format, cache_path=cache_path)
		self.cache_path = cache_path
	
		self.favorites = ['435868', '438814', '436703', '486842', '435896', '437397', '437871', '437869', '437881', '437881',
						  '435724', '437371', '437535', '484362', '483560', '486316', '436950', '437853', '436545', '436575',
						  '495585', '489994', '483330', '436504', '336773', '494509', '265465', '264625', '492389', '340243', '482523']	
		self.ids = []
		self.id_range = (250000,496000)
		self.cur_keyword = 0
		self.query_wait = 2 # seconds
		self.last_query = time()-self.query_wait
		self.base_url = 'http://www.metmuseum.org/art/collection/search/'

		if not os.path.exists(self.cache_path):
			os.makedirs(self.cache_path)

	def get_favorite(self):
		idx = random.randint(0, len(self.favorites)-1)
		self.query(self.favorites[idx])

	def get_random(self):
		met_id = random.randint(self.id_range[0], self.id_range[1])
		self.query(met_id)

	def query(self, met_id):
		if time() - self.last_query > self.query_wait:
			print 'Starting MET image query thread for id:', met_id
			lt = Thread(target=self.load_from_MET, kwargs={'met_id':met_id})
			lt.start()
		else:
			print 'Query denied. Last query:', self.last_query


	def load_from_MET(self, met_id):
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		p = opener.open(self.base_url + met_id)

		page = BeautifulSoup(p)
		a_img_tags = page.findAll('a', {"name":"#collectionImage"})
		match = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", str(a_img_tags))
		if match:
			img_link = match.group(0)
			if img_link[-2:] == "')":
				print 'Got weird apostrophe paren...'
				img_link = img_link[0:-2]

		dl_tags = page.findAll('dl')	
		dd_tags = page.findAll('dd')
		meta_data = dict()
		for dl,dd in zip(dl_tags, dd_tags):
			meta_data[dl.contents[1].contents[0][:-1].encode('ascii','ignore')] = dd.contents[0].encode('ascii','ignore')

		print 'Got MET meta data:\n', meta_data

		mi = METImage(met_id, meta_data, img_link, self.cache_path)
		self.images.append(mi)

class METImage(InternetImage):
	def __init__(self, met_id, meta_data, img_link, cache_path):
		super(METImage, self).__init__(img_link, cache_path)
		self.id = met_id
		self.meta = meta_data





if __name__ == '__main__':
	ism = ImageStreamMET((600,480,3))
	ism.query('436943')
	while True:
		if ism.size() > 0:
			my_img = ism.next()
			cv2.imshow('met img', my_img.to_array())
			cv2.waitKey(0)
		else:
			print "Nothing"
			sleep(4)
