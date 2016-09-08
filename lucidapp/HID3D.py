# HID3D.py
# TouchScreen for LucidTronix eLucidator
# Samwell Freeman
# June 2016

import os
import cv2
import sys
import math
import serial
from time import time, sleep

class HID3D:
	def __init__(self):
		self.last_query = time()
		self.port = serial.Serial('/dev/ttyACM1',9600)

	def listen_loop(self):
		while True:
			read_serial = self.port.readline()
			msg = self.port.readline().strip()
			print "Message is:", msg

	def get_accelerometer(self):
		self.port.write(b'a')
		
		received = ""
		while not 'accelerometer' in received:
			received = self.port.readline()

		splits = received.split(' ')
		x = float(splits[1])
		y = float(splits[2])
		z = float(splits[3])

		return x,y,z


if __name__ == '__main__':
	hid = HID3D()

	while True:
		x,y,z = hid.get_accelerometer()
		print 'Got accelerometer:', x, y, z
		sleep(1)