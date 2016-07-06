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
	def __init__(self, apps, cache_path='./cache/', fullscreen=False, resolution=(500, 400), icon=None, base_graphics='cv2'):
		super(eLucidator, self).__init__('eLucidator', cache_path, fullscreen, resolution, icon, base_graphics)#, cache_path='./cache/', fullscreen=fullscreen, resolution=resolution, icon=None, base_graphics=base_graphics)
		self.apps = apps
		self.active_app = None
		self.ts = lucidapp.TouchScreen()
		self.redraw = True

	def __str__(self):
		return super(eLucidator, self).__str__() + 'eLucidator'

	def open(self):
		pass

	def close(self):
		pass

	def run(self):
		quit = False
		while not quit:
			if self.active_app:
				self.active_app.run()
			else:

				self.ts.update()
				self.handle_keys()

				for b in self.buttons:
					if b.over(self.ts.mx, self.ts.my) and self.ts.double_tap and time()-b.last_press > 0.5:
						ret = b.press()
						if ret < 0:
							quit = True

						self.ts.double_tap = False
					b.show()

				if self.redraw:
					#self.fill()
					self.label('hello', 300, 12)
					self.draw()
					#self.redraw = False


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
	parser.set_defaults(fullscreen=False)
	args = parser.parse_args()
	
	apps = []
	apps.append(lucidapp.GoogleSlider(fullscreen=args.fullscreen))

	lucidator = eLucidator(apps, fullscreen=args.fullscreen)
	lucidator.run()