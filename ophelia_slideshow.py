import pygame
import pygame.ftfont
from pygame import *
from pygame.mixer import *
from pygame.locals import *

import os
import sys
from random import choice
import libtrans
from time import sleep

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
                                        paths.append(os.path.join(path, item))
        return paths

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

def write_text(text, x, y, surface, font, size=1, color=(255,255,255)):
        label = font.render(text, size, color)
        surface.blit(label, (x, y))

def run(resolution=(600,900), fullscreen=False, path=os.environ['HOME']+'/Pictures/ophie/', recursive=True, order=False, delay=3, transition='None'):
        ## Main Function
        ## Runs a slideshow based on parameters given.
        pygame.display.init()
        pygame.ftfont.init()
        myfont = pygame.ftfont.Font(None, 24)

        if fullscreen:
                resolution = pygame.display.list_modes()[0]
                main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
                main_surface = pygame.display.set_mode(resolution)

        write_text("Ophelia Lou Friedman", 10, 10, main_surface, myfont)
        write_text("images from her first year rendered in the style of", 10, 30, main_surface, myfont)
        main_surface.blit(pygame.image.load('/home/sam/Pictures/styles/monalisa.jpg'), (5,50))
        write_text("The Mona Lisa, Leonarado da Vinci", 100, 50, main_surface, myfont)
        pygame.display.update()
        sleep(6)
        main_surface.fill(0)
        write_text("Ophelia Lou Friedman", 10, 10, main_surface, myfont)
        write_text("images from her first year rendered in the style of", 10, 30, main_surface, myfont)
        main_surface.blit(pygame.image.load('/home/sam/Pictures/styles/starry_night.jpg'), (5,50))
        write_text("Starry Night, Vincent Van Gogh", 100, 50, main_surface, myfont)
        pygame.display.update()
        sleep(6)
        main_surface.blit(pygame.image.load('/home/sam/Pictures/styles/picasso.jpg'), (5,50))
        write_text("Girl Before a Mirror, Pablo Picasso", 100, 50, main_surface, myfont)
        pygame.display.update()
        sleep(6)   

        ophie_images = getFilePaths(path, imageTypes, recursive=False)
        mona_images = getFilePaths(path+'mona/', imageTypes, recursive=False)
        van_gogh_images = getFilePaths(path+'van_gogh/', imageTypes, recursive=False)
        picasso_images = getFilePaths(path+'picasso/', imageTypes, recursive=False)

        images = []
        for of in ophie_images:
                images.append(of)
                oname = os.path.splitext(os.path.basename(of))[0]
                for mi in mona_images:
                        if oname in mi:
                                images.append(mi)
                for vi in van_gogh_images:
                        if oname in vi:
                                images.append(vi)
                for pi in picasso_images:
                        if oname in pi:
                                images.append(pi)                                                
        if not len(images) > 0:
                print '\n####  Error: No images found. Exiting!\n'
                sys.exit(1)

	cur_img = 0
	prev_img = -1

	delay *= 1000
	pygame.time.set_timer(pygame.USEREVENT + 1, delay)

	while True:


                for event in pygame.event.get():
                        if (event.type == pygame.QUIT):
                                pygame.quit()
                                return 0
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                                cur_img += 1
                                if cur_img >= len(images):
                                        cur_img = 0
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                                cur_img -=1
                                if cur_img <= -1:
                                        cur_img = len(images) - 1
                        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.quit()
                                return 0
                        elif event.type == pygame.USEREVENT + 1:
                                cur_img += 1
                                if cur_img >= len(images):
                                        cur_img = 0

                if cur_img != prev_img:
                        print 'cur_img is:', cur_img, 'Showing:   ', images[cur_img]
                        blitdata = rationalSizer(pygame.image.load(images[cur_img]), resolution)
                        main_surface = libtrans.transitions[transition](main_surface, blitdata)
                        #main_surface.blit(img, res)
			pygame.display.update()
			prev_img = cur_img




if __name__ == '__main__':
	run(delay=5,transition='Superimposition')
