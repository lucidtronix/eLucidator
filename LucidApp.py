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
import pygame
import pygame.ftfont
from pygame import *
from time import time

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
		self.buttons = []
		self.buttons.append(Button(self, 'exit', (10,10, 45, 20), (25,250, 250), exit_pygame))
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

class Button:
	def __init__(self, app, name, rect, color, callback, icon=None):
		self.app = app
		self.name = name
		self.rect = rect
		self.color = color
		self.callback = callback
		self.icon = icon
		self.last_press = 0

	def show(self):
		if self.app.base_graphics == 'pygame':
			#AAfilledRoundedRect(self.app.surface, self.rect, self.color,0.5)
			pygame.draw.rect(self.app.surface, self.color, self.rect, 0)
		self.app.label(self.name, self.rect[0]+6, self.rect[1])
		pygame.display.update()

	def over(self, x, y):
		return self.rect[0] < x < self.rect[0]+self.rect[2] and self.rect[1] < y < self.rect[1]+self.rect[3]

	def press(self):
		self.last_press = time()
		return self.callback()

def exit_pygame():
	pygame.quit()
	return -1

def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)