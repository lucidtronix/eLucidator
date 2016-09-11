# LucidApp.py
# NYTimesRSS app for LucidTronix eLucidator Applications
# Samwell Freeman
# July 2016

import os
import re
import sys
import cv2
import pygame
import random
import urllib2
import argparse
import threading
import feedparser
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from ImageRow import ImageRow
from bs4 import BeautifulSoup
from cookielib import CookieJar
from TouchScreen import TouchScreen
from LucidApp import LucidApp, Button
from ImageStreamLink import ImageStreamLink

page = BeautifulSoup(urllib2.urlopen("http://www.url.com"))
page.findAll('img')


class NYTimesRSS(LucidApp):

	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(800, 400), icon_path='./icons/nytimes.png', base_graphics='cv2'):
		super(NYTimesRSS, self).__init__('NYTimesRSS', cache_path, fullscreen, resolution, icon_path, base_graphics)
		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()
		self.playing = True
		#self.buttons.append(Button(self, 'more', (100,10,85,40), (50,50,50), self.get_more_images))

		self.max_feeds = 6
		self.science_feeds = self.get_feed()
		self.articles = self.create_articles(self.science_feeds)
		article_buttons = [a.btn for a in self.articles]
		self.buttons += article_buttons


	def __str__(self):
		return 'NYTimesRSS'


	def run(self):
		print ' Start nytimes RSS slider run'
		quit = False

		while not quit:
			self.ts.update()

			ret = self.handle_keys()
			if ret < 0:
				print 'Quit nytimes slider on keys'
				quit = True
				return 0

			self.fill()
			self.label('NYTimes RSS', 205, 40)

			for article in self.articles:
				article.show()

			for b in self.buttons:
				is_over = b.over(self.ts.mx, self.ts.my)
				if is_over and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press()
					if ret < 0:
						print 'Quit nytimes slider on buttons'
						return ret
					self.ts.double_tap = False
				b.show()

			self.draw()


		return 0


	def get_feed(self, feed='feed://rss.nytimes.com/services/xml/rss/nyt/Science.xml'):
		d = feedparser.parse(feed)
		#print d['feed']['title']
		return d.entries
			#print post.title + ": " + post.link


	def create_articles(self, feeds, x=10, y=100):
		articles = []
		for f in feeds[:self.max_feeds]:
			articles.append(Article(f, x, y, self))
			y += 45

		return articles

class Article:
	def __init__(self, feed, x, y, app):
		self.feed = feed
		self.x = x
		self.y = y
		self.app = app
		self.show_me = False
		self.feed.title = self.feed.title.encode('ascii','ignore')

		self.btn = Button(self.app, self.feed.title[:42], (x, y,85,20), (50,50,50), self.toggle_show)
		self.images = [] 
			
		self.keyword = self.feed.title[:12].replace(' ', '_')


		self.keyword_path ='./cache/news/' + self.keyword
		if not os.path.exists(self.keyword_path):
			os.makedirs(self.keyword_path)

		self.row = None

	def get_images(self):
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		p = opener.open(self.feed.link)

		page = BeautifulSoup(p)
		img_tags = page.findAll('img')
		print "Found:", len(img_tags), "images at page:",self.feed.link

		for img in img_tags:
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(img))
			for img_link in urls:
				ii = InternetImage(img_link, self.keyword_path)
				self.images.append(ii)

		return 0

	def toggle_show(self):
		if self.row is None:
			self.stream = ImageStreamLink(self.feed.link, self.keyword)
			self.row = ImageRow(self.app, self.stream, self.app.ts, self.app.resolution)

		self.show_me = not self.show_me
		print self.keyword, 'show:', str(self.show_me)
		return 0	

	def show(self):
		if self.show_me and self.row:
			self.row.update()
			self.row.display()




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	app = NYTimesRSS(fullscreen=args.fullscreen)
	app.run()