# instagram.py

import numpy as np
import urllib
import threading
#import urllib.request as ur
import urllib as ur


import pygame
from pygame import *
from pygame.mixer import *
from pygame.locals import *

from PIL import Image
from io import BytesIO

from time import time, sleep  
from instagram.client import InstagramAPI

access_token ='585822756.695a083.0585d82aaee947edb21bfaf3cf4273de'

api = InstagramAPI(access_token=access_token,  
					client_ips="99.47.41.77",
					client_secret="23eae31d8de84810b9b1344c25ee3a6a")

class InstagramQuery(threading.Thread):
	def __init__(self, images, keyword, type):
		super(InstagramQuery, self).__init__()
		self.images = images
		self.keyword = keyword
		self.type = type
		self.count = 3
	def run(self):
		new_images = []
		if self.type == "tag":
			new_images = get_tag_images(self.keyword, self.count)
		elif self.type == "user":
			new_images = get_user_images(self.keyword, self.count)
		print("Got:"+str(len(new_images))+"in Instagram query thread.")

		if len(new_images) > 0:
			self.images += new_images

class InstagramMedia:
	def __init__(self, media):
		self.media = media
		if media.type == 'image':
			self.pil_image = url_to_image(media.images['standard_resolution'].url)	


def url_to_image(url):
	print("Try to load image:" + url)
	resp = ur.urlopen(url)
	img = Image.open(BytesIO(resp.read()))
	# return the image
	print("Img size:"+str(img.size))
	return img


def get_tag_images(tag="magicegg", count=5):
	print("Load images from tag:" + tag)
	recent_media, url = api.tag_recent_media(tag_name=tag, count=count)
	print("Got recent media.")
	images = []
	for media in recent_media:  
		# Where the media is
		id_ = media.id
		# List of users that like the image
		#users = [user.username for user in media.likes]

		if media.type == 'image':
			#img = url_to_image(media.images['standard_resolution'].url)
			iimg = InstagramMedia(media)
			images.append(iimg)

		sleep(1)
	return images

def get_user_images(user_name, count=5):
	results = api.user_search(user_name, count=2)
	uid = results[0].id
	print('Load images from user:' + user_name+' id:' + uid)
	recent_media, url = api.user_recent_media(user_id=uid, count=count)
        
	images = []
	for media in recent_media:
                # Where the media is
		id_ = media.id
                # List of users that like the image
                #users = [user.username for user in media.likes]
                #print "Likers:", users[:8]
                #print "Media type:", media.type
                #print("Media tags:"+ str(media.tags))
                #print("Media caption:"+ str(media.caption))
		if media.type == 'image':
			iimg = InstagramMedia(media)
			images.append(iimg)
			#img = url_to_image(media.images['standard_resolution'].url)
			#images.append(img)	

			sleep(1)
	return images	

def pil_image_to_surface(img):
	mode = img.mode
	size = img.size
	data = img.tostring()
	#print ("mode is"+str(img.mode))
	#assert mode in "RGB", "RGBA"
	
	surface = pygame.image.fromstring(data, size, mode)
	return surface


def instagram_frame():
	resolution = (900, 900)
	fullscreen = False #True
	last_update = 0
	last_load = 0
	load_wait_interval = 1200

	pygame.display.init()
	pygame.font.init()
	myfont = pygame.font.Font(None, 36)
	
	cur_user = 0
	users = ["meoremy", "samwell3", "omg.rb.md", "moistbuddha", "butterknuckles", "peanutbutterpear"]
	cur_tag = 0
	tags = ["magic egg",  "fractals", "news", "beauty", "time", "reflection"]
	loaded = []

	if fullscreen:
		resolution = pygame.display.list_modes()[0]
		main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
	else:
		main_surface = pygame.display.set_mode(resolution)
	
	label = myfont.render("Hello", 1, (255,255,0))
	main_surface.blit(label, (20, 400))
	#main_surface.blit(pygame.image.load('/home/pi/python_games/boy.png'), (100,50))
	pygame.display.update()
	#images = [Image.open('/home/sam/python_games/boy.png')] 
	images = [] #[Image.open('/home/sam/Dropbox/Photos/k8/IMG_0540.jpg')]
	#images = get_user_images(users[cur_user], 3)
	#loaded.append(users[cur_user])
	print("Loaded:"+str(len(images))+"images")
	cur_image = len(images)-1
	playing = True
	while True:
		#handle_events(images)
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return 0
			elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				return 0
			elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
				cur_image += 1
				if cur_image >= len(images):
					cur_image = 0
				print("Cur images is now:"+str(cur_image)+"of:"+str(len(images)))
				last_update = 0
			elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
				cur_user += 1
				if cur_user >= len(users):
					cur_user = 0
				if users[cur_user] not in loaded:
					iq = InstagramQuery(images, users[cur_user], "user")
					iq.start()
					#images += get_user_images(users[cur_user], 3)
					loaded.append(users[cur_user])
			elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
				cur_tag += 1
				if cur_tag >= len(tags):
					cur_tag = 0
				if tags[cur_tag] not in loaded:
					#images += get_tag_images(tags[cur_tag], 3)
					iq = InstagramQuery(images, tags[cur_tag], "tag")
					iq.start()
					loaded.append(tags[cur_tag])

		if time() - last_load > load_wait_interval:
			print("loading new triggered...")
			cur_user += 1
			if cur_user >= len(users):
				cur_user = 0
			if users[cur_user] not in loaded:
				iq = InstagramQuery(images, users[cur_user], "user")
				iq.start()
				loaded.append(users[cur_user])
			last_load = time()

		if len(images) > 0 and time() - last_update > 3:
			if playing:
				cur_image = 1 + cur_image
				if cur_image >= len(images):
					cur_image = 0
			iimg = images[cur_image]
			img_surf = pil_image_to_surface(iimg.pil_image)
			main_surface.blit(img_surf, (0,0))

			label = myfont.render(str(iimg.media.caption), 1, (255,255,0))		
			main_surface.blit(label, (20, 400))

			pygame.display.update()
			last_update = time()

if __name__ == '__main__':
	#print inspect.getmembers(api)
	#get_by_user("omg.rb.md")
	instagram_frame()
