#!/usr/bin/env python
# eLucidator.py
# Python Skin for Lucidtronix' eLucidator
# Meta-file which displays and calls LucidApps
# Samwell Freeman
# July 2016

import os
import sys
import cv2
import argparse
import lucidapp
from time import time

screen_width = 800
screen_height = 480

class eLucidator(lucidapp.LucidApp):
	def __init__(self, apps, ts, cache_path=lucidapp.defines.base_path+'cache/', fullscreen=False, resolution=(800, 480), icon=None, base_graphics='cv2'):
		super(eLucidator, self).__init__('eLucidator', cache_path, fullscreen, resolution, icon)
		self.apps = apps
		self.init_app_buttons()

		self.ts = ts
		self.redraw = True	

	def __str__(self):
		return super(eLucidator, self).__str__() + 'eLucidator'

	def open(self):
		pass

	def close(self):
		pass

	def init_app_buttons(self):
		bx = 10
		by = 70
		bw = 250
		bh = 40

		for app in self.apps:
			self.buttons.append(lucidapp.Button(self, str(app), (bx,by,bw,bh), (150,150,150), app.run, app.icon))
			by += 55

	def run(self, run_app=""):
		for app in self.apps:
			if app.name == run_app:
				app.run()
				
		quit = False
		while not quit:

				self.ts.update()

				ret = self.handle_keys()
				if ret <= 0:
					quit = True
				
				for b in self.buttons:
					if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
						ret = b.press()
						if ret < 0:
							quit = True

						self.ts.double_tap = False
					b.show()

				self.draw()

		cv2.destroyAllWindows()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true', default=True)
	parser.add_argument('--run', dest='run')

	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	
	apps = []

	if args.fullscreen:
		cv2.namedWindow("canvas", cv2.WINDOW_NORMAL)          
		cv2.setWindowProperty("canvas", cv2.WND_PROP_FULLSCREEN, 1)
	else:
		cv2.namedWindow("canvas")

	ts = lucidapp.TouchScreen()
	res = (screen_width, screen_height)
	

	apps.append(lucidapp.SlideshowTouch(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.ImagenetViewer(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.SlideshowMET(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.GoogleSlider(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.ImageSlider(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.NYTimesRSS(ts=ts, fullscreen=args.fullscreen, resolution=res))
	apps.append(lucidapp.Mandelbrot(ts=ts, fullscreen=args.fullscreen, resolution=res))
	#apps.append(lucidapp.BallBounce(ts=ts, fullscreen=args.fullscreen, resolution=res))

	try:
		apps.append(lucidapp.CVClient(ts=ts, fullscreen=args.fullscreen))
	except:
		print 'Could not load cv client'

	lucidator = eLucidator(apps, ts=ts, fullscreen=args.fullscreen, resolution=res)
	lucidator.run(args.run)

	cv2.destroyAllWindows()
