# face_detection_stub.py
# Written by Samwell Freeman
# March 2016

import cv2
import sys
import os
import numpy as np

from cStringIO import StringIO

def draw_loop():
	cascPath = sys.argv[1]
	faceCascade = cv2.CascadeClassifier(cascPath)

	video_capture = cv2.VideoCapture(0)

	while True:
		# Capture frame-by-frame
		frame = np.zeros((720, 1280, 3), np.uint8)
		ret = video_capture.grab()

		if ret:
			retc, frame = video_capture.retrieve()
			print frame.shape
			if not(retc):
				print 'Could not get image capture try different device number in cv2.VideoCapture(0)'		
			else:
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				faces = faceCascade.detectMultiScale(
					gray,
					scaleFactor=1.1,
					minNeighbors=5,
					minSize=(30, 30),
					flags=cv2.CASCADE_SCALE_IMAGE
				)

				# Draw a rectangle around the faces
				for (x, y, w, h) in faces:
					#face = frame[y:y+h, x:x+w]
					#stable_face[0:min(stable_size,h), 0:min(stable_size,w)] = face[0:min(stable_size,h), 0:min(stable_size,w)]
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
					#cv2.imshow('Face', face)
				cv2.imshow('canvas', frame)

				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

	# When everything is done, release the capture
	video_capture.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	draw_loop()
