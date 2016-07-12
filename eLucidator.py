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

class eLucidator(lucidapp.LucidApp):
	def __init__(self, apps, ts, cache_path='./cache/', fullscreen=False, resolution=(500, 400), icon=None, base_graphics='cv2'):
		super(eLucidator, self).__init__('eLucidator', cache_path, fullscreen, resolution, icon, base_graphics)#, cache_path='./cache/', fullscreen=fullscreen, resolution=resolution, icon=None, base_graphics=base_graphics)
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
		bw = 200
		bh = 40

		for app in self.apps:
			self.buttons.append(lucidapp.Button(self, str(app), (bx,by,bw,bh), (150,150,150), app.run))
			by += 55


	def run(self):
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
				ax = 220
				ay = 80
				for app in self.apps:
					self.show_image_cv(app.icon, (ax, ay))
					ay += 55
				
				self.draw()

		cv2.destroyAllWindows()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	
	apps = []

	if args.fullscreen:
		cv2.namedWindow("canvas", cv2.WINDOW_NORMAL)          
		cv2.setWindowProperty("canvas", cv2.WND_PROP_FULLSCREEN, 1)
	else:
		cv2.namedWindow("canvas")

	ts = lucidapp.TouchScreen()
	apps.append(lucidapp.GoogleSlider(ts=ts, fullscreen=args.fullscreen))
	apps.append(lucidapp.ImageSlider(ts=ts, fullscreen=args.fullscreen))
	try:
		apps.append(lucidapp.FaceDetector(ts=ts, fullscreen=args.fullscreen))
	except:
		print 'Could not load face detector'
	lucidator = eLucidator(apps, ts=ts, fullscreen=args.fullscreen)
	lucidator.run()

	cv2.destroyAllWindows()