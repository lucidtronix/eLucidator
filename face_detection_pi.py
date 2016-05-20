# face_detection_pi.py
# Written by Samwell Freeman
# March 2016

import cv2
import sys
import os
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def draw_loop():
	cascPath = sys.argv[1]
	faceCascade = cv2.CascadeClassifier(cascPath)

	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (320, 240)
        camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(320, 240))

        # allow the camera to warmup
	time.sleep(0.1)

	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        	# grab the raw NumPy array representing the image, then initialize the timestamp
        	# and occupied/unoccupied text
		image = frame.array
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
                                        gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(30, 30),
                                        flags=cv2.CASCADE_SCALE_IMAGE
                                )

                # Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)

        	# show the frame
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

       		 # if the `q` key was pressed, break from the loo
		if key == ord("q"):
			break


	cv2.destroyAllWindows()

if __name__ == '__main__':
	draw_loop()
