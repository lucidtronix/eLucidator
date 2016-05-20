import pygame
from pygame import *
from pygame.mixer import *
from pygame.locals import *
import os
import sys
import random
import libtrans

imageTypes = ['.jpg', '.jpeg', '.png']

def getFilePaths(path, fileTypes, recursive=True):
        ## Returns list containing paths of files in /path/ that are of a file type in /fileTypes/,
        ##      if /recursive/ is False subdirectories are not checked.
        paths = []
        if recursive:
                for root, folders, files in os.walk(path, followlinks=True):
                        for file in files:
                                for fileType in fileTypes:
                                        if file.endswith(fileType):
                                                paths.append(os.path.join(root, file))
        else:
                for item in os.listdir(path):
                        for fileType in fileTypes:
                                if item.endswith(fileType):
                                        paths.append(os.path.join(root, item))
        return paths


class DreamImages:
	def __init__(self, net_name, base_path, images_2_dreams):
		self.net_name = net_name
		self.base_path = base_path
		self.images_2_dreams = images_2_dreams
		self.image_indices = {}
		self.base_index = random.randint(0, len(images_2_dreams.keys())-1)
		for i in range(len(images_2_dreams.keys())):
			self.image_indices[i] = 0
		
		self.dreaming = False
		print "Made net:", net_name, " imag idxs ", len(images_2_dreams.keys()), "and:", len(self.image_indices.keys())

	def get_next_image(self):
		image_path = self.base_path
		cur_base = self.images_2_dreams.keys()[self.base_index]

		if self.dreaming:
			cur_dreams = self.images_2_dreams[cur_base]
			print "cur dream len:", len(cur_dreams), " base idx:", self.base_index, " cur base:", cur_base
			dream_idx = self.image_indices[self.base_index]
			image_path += cur_base + '/' + cur_dreams[dream_idx]
			self.image_indices[self.base_index] += 1
			if self.image_indices[self.base_index] == len(cur_dreams):
				self.image_indices[self.base_index] = 0
                        self.base_index += 1
                        if self.base_index == len(self.images_2_dreams.keys()):
                                self.base_index = 0

		else:
			image_path += cur_base + '/' + cur_base
			
		self.dreaming = not self.dreaming
		return image_path


def get_image_dict(path, extensions):
	dream_image_dict = {}
	for net_name in os.listdir(path):
		print "Net_name is:", net_name
		net_dict = {}
		for base_image in os.listdir(path+net_name):
			if base_image[0] == '.':
				continue
			net_dict[base_image] = []
			net_path = path + net_name + '/'
			for dream_image in os.listdir(net_path+base_image):
				if dream_image[0] == '.' or dream_image == base_image:
					continue
				for ext in extensions:
					if dream_image.endswith(ext):
						net_dict[base_image].append(dream_image)
			if len(net_dict[base_image]) < 2:
				del net_dict[base_image]
		print "Net dict len:", len(net_dict.keys()) 
		dream_image_dict[net_name] = DreamImages(net_name, net_path, net_dict)
	return dream_image_dict

def rationalSizer(image, area):
        ## Returns /image/ resized for /area/ maintaining origional aspect ratio.
        ## Returns tuple containing x and y displacement to center resized /image/ correctly on /area/.
        width = float(image.get_width())
        height = float(image.get_height())
        xSizer = width / area[0]
        ySizer = height / area[1]
        if xSizer >= ySizer:
                sizer = xSizer
                yDisplace = int((area[1] - height/xSizer) / 2)
                xDisplace = 0
        else:
                sizer = ySizer
                xDisplace = int((area[0] - width/ySizer) / 2)
                yDisplace = 0
        return pygame.transform.scale(image, (int(width/sizer),int(height/sizer))), (xDisplace, yDisplace)

def run(resolution=(1200,900), fullscreen=True, path='/home/pi/Pictures/', delay=3, transition='None'):
        ## Main Function
        ## Runs a slideshow based on parameters given.
        pygame.display.init()
        if fullscreen:
                resolution = pygame.display.list_modes()[0]
                main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
                main_surface = pygame.display.set_mode(resolution)

        pygame.display.update()
	net_dreams = get_image_dict(path, imageTypes)
        if not len(net_dreams.keys()) > 0:
                print '\n####  Error: No images found. Exiting!\n'
                sys.exit(1)

	net_idx = 0
	cur_net = net_dreams.keys()[net_idx]

	delay *= 1000
	pygame.time.set_timer(pygame.USEREVENT + 1, delay)

	while True:
		get_new_image = False
                for event in pygame.event.get():
                        if (event.type == pygame.QUIT):
                                pygame.quit()
                                return 0
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                                print "right arrow"
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                                print "left arrow"
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.quit()
                                return 0
                        elif event.type == pygame.USEREVENT + 1:
                                get_new_image = True
				if not net_dreams[cur_net].dreaming:
					net_idx += 1
					if net_idx == len(net_dreams.keys()):
						net_idx = 0

                if get_new_image:
			cur_net = net_dreams.keys()[net_idx]
			image_path = net_dreams[cur_net].get_next_image()
                        print '\nShowing new image', image_path
			 
                        blitdata = rationalSizer(pygame.image.load(image_path), resolution)
                        main_surface = libtrans.transitions[transition](main_surface, blitdata)
                        #main_surface.blit(img, res)
			pygame.display.update()
			

if __name__ == '__main__':
	run(delay=7,transition='Superimposition')
