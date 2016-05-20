# feed_parser_stub.py
# Written by Samwell Freeman
# March 2016

import sys
import os
import feedparser
import numpy as np
import pygame
import pygame.ftfont
import urllib2
from cookielib import CookieJar
import webbrowser

class Article:
	def __init__(self, feed, x, y, surface, font):
		self.feed = feed
		self.x = x
		self.y = y
		self.surface = surface
		self.font = font


	def show_title(self):
		mx, my = pygame.mouse.get_pos()
		if (self.over(mx, my)):
			write_text(self.feed.title, self.x, self.y, self.surface, self.font, color=(255,0,20))
			b1, b2, b3 = pygame.mouse.get_pressed()
			if b1:
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
			write_text(self.feed.title, self.x, self.y, self.surface, self.font)


	def over(self, mx, my):
		t_width, t_height = self.font.size(self.feed.title)
		if(mx > self.x and mx < self.x + t_width and my > self.y and my < self.y + t_height):
			return True
		return False


def get_feed(feed='feed://rss.nytimes.com/services/xml/rss/nyt/Science.xml'):
	d = feedparser.parse(feed)
	#print d['feed']['title']
	return d.entries
		#print post.title + ": " + post.link

def write_text(text, x, y, surface, font, size=1, color=(255,255,255)):
	label = font.render(text, size, color)
	surface.blit(label, (x, y))

def create_articles(feeds, surface, font, x=10, y=10):
	articles = []
	for f in feeds:
		articles.append(Article(f, x, y, surface, font))
		y += 25

	return articles



def run(resolution=(1200,900), fullscreen=False):
	## Main Function
	pygame.display.init()
	pygame.ftfont.init()
	myfont = pygame.ftfont.Font(None, 36)
	science_feeds = get_feed()
	if fullscreen:
			resolution = pygame.display.list_modes()[0]
			main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
	else:
			main_surface = pygame.display.set_mode(resolution)

	articles = create_articles(science_feeds, main_surface, myfont)



	while True:
		main_surface.fill(0)
		for a in articles:
			a.show_title()
		pygame.display.update()
			

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return 0



if __name__ == '__main__':
	run()