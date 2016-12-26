# Lucid Apps __init__.py
import defines

from LucidApp import LucidApp, Button
from ImageSlider import ImageSlider
from GoogleSlider import GoogleSlider
from TouchScreen import TouchScreen
from Slideshow import Slideshow
from SlideshowMET import SlideshowMET
from SlideshowTouch import SlideshowTouch
from ImagenetViewer import ImagenetViewer
from NYTimesRSS import NYTimesRSS
from BallBounce import BallBounce
from Mandelbrot import Mandelbrot

try:
	from FaceDetector import FaceDetector
	from CVClient import CVClient	
except:
	print 'could not load face detector or CV Client'