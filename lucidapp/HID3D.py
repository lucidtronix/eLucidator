# HID3D.py
# TouchScreen for LucidTronix eLucidator
# Samwell Freeman
# June 2016

import os
import cv2
import sys
import math
import serial
from time import time

class HID3D:
	def __init__(self):
		self.last_query = time()