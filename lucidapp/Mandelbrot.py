# Mandelbrot.py
# Mandelbrot Class for LucidTronix eLucidator
# Samwell Freeman
# September 2016

import os
import sys
import cv2
import math
import pygame
import colorsys
import threading
import numpy as np
from time import time
from PIL import Image
import urllib, cStringIO
from LucidApp import LucidApp, Button
from TouchScreen import TouchScreen
from ImageStreamDir import ImageStreamDir

class Mandelbrot(LucidApp):
	def __init__(self, ts=None, cache_path='./cache/', fullscreen=False, 
					resolution=(800, 400), icon_path='./icons/Mandelbrot.png'):
		
		super(Mandelbrot, self).__init__('Mandelbrot', cache_path, fullscreen, resolution, icon_path)
		
		self.ts = ts if ts else TouchScreen()
		self.last_update = time() 
		#self.buttons.append(Button(self, 'next', (260,10,80,40), (50,50,50), self.next))
		#self.buttons.append(Button(self, 'previous', (100,10,145,40), (50,50,50), self.prev_image))
		self.cur_color = (128,128,128)
		self.bg_color = (0,0,0)
		self.mandelbrot_image = np.zeros((self.resolution[1] - 20, self.resolution[0] -20, 3))
		self.x_range = (-0.74888, -0.74877)   # (-2.0, 0.5) # 
		self.y_range =  (0.06515, 0.06525)# (-1.5, 1.5) # 
		self.zoom = 1.0
		self.maxiter = 1024
		self.cur_x = 0
		self.cur_y = 0

	def __str__(self):
		return 'Mandelbrot'


	def run(self):
		quit = False
		while not quit:
			self.ts.update()

			ret = self.handle_keys()
			if ret < 0:
				quit = True

			for b in self.buttons:
				if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
					ret = b.press() 
					if ret < 0:
						quit = True
					self.ts.double_tap = False
				b.show()
			
			x_ratio = float(self.cur_x) / self.mandelbrot_image.shape[0]
			scale_x = self.x_range[0] + x_ratio*(self.x_range[1]-self.x_range[0])
			y_ratio = float(self.cur_y) / self.mandelbrot_image.shape[1]
			scale_y = self.y_range[0] + y_ratio*(self.y_range[1]-self.y_range[0])            

			z = scale_x + 1j*scale_y 
			f_of_z = mandelbrot(z, self.maxiter)

			self.canvas[self.cur_x,self.cur_y,:] = i_to_rgb(f_of_z)
			
			self.cur_x += 1
			if self.cur_x >= self.mandelbrot_image.shape[0]:
				self.cur_y += 1
				self.cur_x = 0
				if self.cur_y >= self.mandelbrot_image.shape[1]:
					self.cur_y = 0
					self.cur_x = 0
			
			self.label(self.name, 70, 300, font_scale=1.5, alpha = 0.5)
			self.draw()


# resolution = (1024, 1024, 3)

def i_to_rgb(i):
  color = 255 * np.array(colorsys.hsv_to_rgb(i/255.0, 1.0, 0.5))
  return color.astype(int)

def mandelbrot(z,maxiter):
  c = z
  for n in range(maxiter):
      if abs(z) > 2:
          return n
      z = z*z + c
  return maxiter

# def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
#     r1 = np.linspace(xmin, xmax, width)
#     r2 = np.linspace(ymin, ymax, height)
#     n3 = np.empty((width,height, 3))
#     for i in range(width):
#         for j in range(height):
#             m = mandelbrot(r1[i] + 1j*r2[j],maxiter)
#             n3[i,j,:] = i_to_rgb(m)
#     return n3


# def run_m2(width,height):

#   #img = mandelbrot_set(-2.4,0.5,-1.25,1.25,resolution[0], resolution[1], 1024)
#   img = mandelbrot_set(-0.74888, -0.74877, 0.06515, 0.06525, width, height, 1200)
#   print 'got img shape:', img.shape, 'min: ', img.min(), 'max:',  img.max()
#   img -= img.min()
#   img *=  255.0/img.max()
#   img = np.uint8(img)
#   while True:
#     cv2.imshow('Image', img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#       break

if __name__ == '__main__':
	app = Mandelbrot()
	app.run()
