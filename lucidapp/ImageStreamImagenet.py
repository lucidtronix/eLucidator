# ImageStreamImagenet.py
# Written by Samwell Freeman
# October 2016

import os
import re
import sys
import cv2
import random
import defines
import numpy as np
from PIL import Image
import urllib2, cStringIO
from time import time, sleep
from threading import Thread
from bs4 import BeautifulSoup
from cookielib import CookieJar
from ImageStream import ImageStream, InternetImage


class ImageStreamImagenet(ImageStream):
	def __init__(self, cache_path=defines.base_path+'cache/imagenet/'):
		super(ImageStreamImagenet, self).__init__('Imagenet', cache_path=cache_path)
	
		self.ids = []
		self.query_wait = 2 # seconds
		self.last_query = time()-self.query_wait
		self.imagenet_dir = '/home/sam/big_data/imagenet/'
		
		self.cache_path = cache_path
		if not os.path.exists(self.cache_path):
			os.makedirs(self.cache_path)

	def load_val_images(self, limit=135):
		v_img_path = self.imagenet_dir + 'ILSVRC2013_DET_val/'
		v_xml_path = self.imagenet_dir + 'ILSVRC2013_DET_bbox_val/'
		vd = sorted(os.listdir(v_img_path))
		xmld = sorted(os.listdir(v_xml_path))

		count = 0
		for val_img, xml_file in zip(vd, xmld):
			assert xml_file[:-4] in val_img
			bs_xml = BeautifulSoup(open(v_xml_path + xml_file, 'r'))

			meta_data = {}
			try:
				meta_data["xmin"] = int(bs_xml.findAll("xmin")[0].contents[0])
				meta_data["xmax"] = int(bs_xml.findAll("xmax")[0].contents[0])
				meta_data["ymin"] = int(bs_xml.findAll("ymin")[0].contents[0])
				meta_data["ymax"] = int(bs_xml.findAll("ymax")[0].contents[0])

				imagenet_id = bs_xml.findAll("name")[0].contents[0]
				meta_data["word"] = word_from_imagenet_id(imagenet_id).replace('\n', ' ')
				print 'imagenet_id', imagenet_id, 'word is' , meta_data["word"]
				ii = ImagenetImage(imagenet_id, meta_data, v_img_path + val_img)
				self.images.append(ii)
				count +=1
				if count == limit:
					break
			except:
				print "Error... xml missing bounding box maybe?", xml_file, ' bs xml:', bs_xml, ' meta', meta_data
				continue



	def query(self):
		if time() - self.last_query > self.query_wait:
			print 'Starting Imagenet image query thread'
			lt = Thread(target=self.load_val_images)
			lt.start()
		else:
			print 'Query denied. Last query:', self.last_query




def word_from_imagenet_id(imagenet_id):
	wnet_url = 'http://www.image-net.org/api/text/wordnet.synset.getwords?wnid=' + imagenet_id
	word = cStringIO.StringIO(urllib2.urlopen(wnet_url).read())
	return word.getvalue()

def word_to_imagenet_id(word):
	wnet_url = 'http://www.image-net.org/api/text/wordnet.synset.getwords?wnid=' + imagenet_id
	word = cStringIO.StringIO(urllib2.urlopen(wnet_url).read())
	return word.getvalue()

def hyponym_from_imagenet_id(imagenet_id, full=False):
	''' 
	Returns an array of imagenet_ids that are 
	semantic children or progeny of the given imagenet_id 
	if Parameter full is true we return all progeny otherwise just the children
	'''
	
	wnet_url = 'http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=' + imagenet_id
	if full:
		wnet_url += '&full=1'

	id_file = cStringIO.StringIO(urllib2.urlopen(wnet_url).read())
	return id_file.getvalue().split('\n')

def shuffle_in_unison_inplace(a, b):
	assert len(a) == len(b)
	p = np.random.permutation(len(a))
	return a[p], b[p]

def download_synset(imagenet_id):
	synset_url = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=' + imagenet_id

	id_file = cStringIO.StringIO(urllib.urlopen(synset_url).read())
	url_array = id_file.getvalue().split('\n')

	for img_url in url_array:
		cache_path = data_path + imagenet_id +'/' + img_url.replace("http://", "").replace("/", "__").strip()
		if(os.path.isfile(cache_path)):
			print 'Already downloaded image. At:', cache_path
		else:
			try:
				file = cStringIO.StringIO(urllib2.urlopen(img_url).read())
				img = Image.open(file)
				cdir = os.path.dirname(cache_path)
				
				if not os.path.exists(cdir):
					os.makedirs(cdir)  
				
				img.save(cache_path)
				print 'Saved image at:', cache_path
			except:
				print 'Error reading:', img_url



class ImagenetImage(InternetImage):
	def __init__(self, imagenet_id, meta_data, cache_path, crop=(500,400)):
		super(ImagenetImage, self).__init__(cache_path, crop=crop)
		self.id = imagenet_id
		self.meta = meta_data


if __name__ == '__main__':
	ism = ImageStreamImagenet()
	ism.query()
	while True:
		if ism.size() > 0:
			my_img = ism.next()
			cv2.imshow('imagenet img', my_img.to_array())
			cv2.waitKey(0)
		else:
			print "Nothing"
			sleep(4)
