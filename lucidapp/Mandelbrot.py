# Mandelbrot.py
# Mandelbrot Class for LucidTronix eLucidator
# Samwell Freeman
# September 2016

import os
import sys
import cv2
import math
import defines
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
	def __init__(self, ts=None, cache_path=defines.base_path+'cache/', fullscreen=False, 
					resolution=(800, 400), icon_path=defines.base_path+'icons/Mandelbrot.png'):
		
		super(Mandelbrot, self).__init__('Mandelbrot', cache_path, fullscreen, resolution, icon_path)
		
		self.ts = ts if ts else TouchScreen()
		self.last_update = time() 
		#self.buttons.append(Button(self, 'next', (260,10,80,40), (50,50,50), self.next))
		self.cur_color = (128,128,128)
		self.bg_color = (0,0,0)

		# x1, x2, y1, y2
		self.mandelbrot_shape = (20, 450, 90, 310)
		self.x_range = (-0.74888, -0.74877)   # (-2.0, 0.5) # 
		self.y_range =  (0.06515, 0.06525)# (-1.5, 1.5) # 
		#self.x_range = (-2.0, 0.5) # 
		#self.y_range = (-1.5, 1.5) # 
		self.zoom = 1.0
		self.maxiter = 1024
		self.cur_x = 0
		self.cur_y = 0
		self.level = 1

	def __str__(self):
		return 'Mandelbrot'


	def run(self):
		quit = False
		tiles_at_this_level = 2**self.level
		xpix = self.mandelbrot_width() / tiles_at_this_level
		ypix = self.mandelbrot_height() / tiles_at_this_level
		self.label(self.name, 70, 320, font_scale=1.1)

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
			

			x1 = self.cur_x*xpix
			x2 = (self.cur_x+1)*xpix
			y1 = self.cur_y*ypix
			y2 = (self.cur_y+1)*ypix
			
			self.color_tile((x1,x2,y1,y2))

			self.cur_x += 1
			if x2 >= self.mandelbrot_shape[1]-xpix:
				self.cur_y += 1
				self.cur_x = 0
				if y2 >= self.mandelbrot_shape[3]-ypix:
					self.cur_y = 0
					self.cur_x = 0
					self.level += 1
					tiles_at_this_level = 2**self.level
					xpix = max(1, self.mandelbrot_width() / tiles_at_this_level)
					ypix = max(1, self.mandelbrot_height() / tiles_at_this_level)

					print 'going to next level:', self.level, 'tiles here:', tiles_at_this_level, 'xpix:', xpix, 'ypix:', ypix
			
			self.draw()

	def mandelbrot_width(self):
		return self.mandelbrot_shape[1]-self.mandelbrot_shape[0]

	def mandelbrot_height(self):
		return self.mandelbrot_shape[3]-self.mandelbrot_shape[2]
		
 
	def color_tile(self, tile):
		sample_x = (tile[0] + tile[1]) / 2
		sample_y = (tile[2] + tile[3]) / 2

		yb1 = self.mandelbrot_shape[2]+tile[2]
		yb2 = self.mandelbrot_shape[2]+tile[3]
		xb1 = self.mandelbrot_shape[0]+tile[0]
		xb2 = self.mandelbrot_shape[0]+tile[1]

		self.canvas[yb1:yb2, xb1:xb2, :] = self.color_from_point(sample_x, sample_y)

	def color_from_point(self, x, y):
		x_ratio = float(x) / self.mandelbrot_width()
		scale_x = self.x_range[0] + x_ratio*(self.x_range[1]-self.x_range[0])
		y_ratio = float(y) / self.mandelbrot_height()
		scale_y = self.y_range[0] + y_ratio*(self.y_range[1]-self.y_range[0])            

		z = scale_x + 1j*scale_y 
		f_of_z = mandelbrot(z, self.maxiter)

		return i_to_rgb(f_of_z)	


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

if __name__ == '__main__':
	app = Mandelbrot()
	app.run()
