# LucidApp.py
# NYTimesRSS app for LucidTronix eLucidator Applications
# Samwell Freeman
# July 2016

import os
import sys
import cv2
import pygame
import random
import urllib2
import argparse
import threading
import feedparser
import webbrowser
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from cookielib import CookieJar
from TouchScreen import TouchScreen
from LucidApp import LucidApp, Button
from ImageStreamDir import ImageStreamDir

class NYTimesRSS(LucidApp):

	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, resolution=(800, 400), icon_path='./icons/ny_times.png', base_graphics='cv2'):
		super(NYTimesRSS, self).__init__('NYTimesRSS', cache_path, fullscreen, resolution, icon_path, base_graphics)
		if ts:
			self.ts = ts
		else:
			self.ts = TouchScreen()
		self.playing = True
		#self.buttons.append(Button(self, 'more', (100,10,85,40), (50,50,50), self.get_more_images))

		self.science_feeds = self.get_feed()
		self.articles = self.create_articles(self.science_feeds)

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
				return 0

			self.fill()
			self.label('NYTimes RSS', 205, 40)

			for b in self.buttons:
				is_over = b.over(self.ts.mx, self.ts.my)
				if is_over and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press()
					if ret < 0:
						print 'Quit nytimes slider on buttons'
						return ret
					self.ts.double_tap = False
				b.show()

			for a in self.articles:
				a.show_title()

			self.draw()

		return 0


	def get_feed(self, feed='feed://rss.nytimes.com/services/xml/rss/nyt/Science.xml'):
		d = feedparser.parse(feed)
		#print d['feed']['title']
		return d.entries
			#print post.title + ": " + post.link


	def create_articles(self, feeds, x=10, y=70):
		articles = []
		for f in feeds:
			articles.append(Article(f, x, y, self))
			y += 25

		return articles

class Article:
	def __init__(self, feed, x, y, app):
		self.feed = feed
		self.x = x
		self.y = y
		self.app = app
		self.feed.title = self.feed.title.encode('ascii','ignore')
	def show_title(self):
		if (self.over(self.app.ts.mx, self.app.ts.my)):
			self.app.label(self.feed.title, self.x, self.y)

			if self.app.ts.double_tap:
				webbrowser.open(self.feed.link)
				# cj = CookieJar()
				# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
				# p = opener.open(self.feed.link)

				# # print "Try to read url", self.feed.link
				# # req = urllib2.Request(self.feed.link)
				# # print "Got request"
				# # response = urllib2.urlopen(req)
				# # print "Got respone"

				# # html = response.read()
				# print p.read()

		else:
			self.app.label(self.feed.title, self.x, self.y)

	def over(self, mx, my):
		t_width, t_height = 150, 20
		if(mx > self.x and mx < self.x + t_width and my > self.y and my < self.y + t_height):
			return True
		return False





if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	app = NYTimesRSS(fullscreen=args.fullscreen)
	app.run()