# LucidApp.py
# Base Class for LucidTronix eLucidator Applications
# Samwell Freeman
# June 2016

import os
import sys
import cv2
import threading
import numpy as np
from PIL import Image
import urllib, cStringIO
from time import time
import pygame
import pygame.ftfont


class LucidApp(object):
	def __init__(self, name, cache_path='./cache/', fullscreen=False, resolution=(400, 300), icon=None, base_graphics='pygame'):
		super(LucidApp, self)
		self.name = name 
		self.cache_path = cache_path
		self.recording = False
		self.fullscreen = fullscreen
		self.resolution = resolution
		self.playing = True
		self.icon = icon
		self.base_graphics = base_graphics
		if self.base_graphics == 'pygame':
			self.pygame_init()

	def __str__(self):
		return "LucidApp:" +  self.name

	def open(self):
		pass

	def close(self):
		pass

	def loop(self):
		pass

	def pygame_init(self):
		pygame.display.init()
		pygame.ftfont.init()
		self.py_font = pygame.ftfont.Font(None, 24)

		if self.fullscreen:
			self.resolution = pygame.display.list_modes()[0]
			self.surface = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
		else:
			self.surface = pygame.display.set_mode(self.resolution)		

	def label(self, text, x, y, size=1, color=(255,255,255)):
		if self.base_graphics == 'pygame':
			my_label = self.py_font.render(text, size, color)
			self.surface.blit(my_label, (x, y))