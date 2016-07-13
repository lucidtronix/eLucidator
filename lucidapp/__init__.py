# Lucid Apps __init__.py
from LucidApp import LucidApp, Button
from ImageSlider import ImageSlider
from GoogleSlider import GoogleSlider
from TouchScreen import TouchScreen
from Slideshow import Slideshow
try:
	from FaceDetector import FaceDetector
except:
	print 'could not load face detector'