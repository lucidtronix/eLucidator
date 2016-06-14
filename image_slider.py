# image_slider.py
# Written by Samwell Freeman
# LucidTronix, June 2016

import os
from time import time
import pygame
import pygame.ftfont

def write_text(text, x, y, surface, font, size=1, color=(255,255,255)):
	label = font.render(text, size, color)
	surface.blit(label, (x, y))

def run(images_path ='./images/', fullscreen=False):
	imgs = os.listdir(images_path)
	pyimgs = []
	for img in imgs:
		pyimgs.append(pygame.image.load(images_path+img))

	pygame.display.init()
	pygame.ftfont.init()
	font = pygame.ftfont.Font(None, 24)

	if fullscreen:
		resolution = pygame.display.list_modes()[0]
		main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
	else:
		main_surface = pygame.display.set_mode((500, 400))

	sliding = False
	sx = sy = dx = cx = 0
	b0_begin = b1_begin = 0
	last_hold = last_up = 1.0
	cur_img = 0
	while True:
		main_surface.fill(0)
		mx, my = pygame.mouse.get_pos()
		b1, b2, b3 = pygame.mouse.get_pressed()

		if b1:
			if not sliding:
				last_up = time()-b0_begin
				b1_begin = time()
				sliding = True
				sx = mx
				sy = my
			dx = mx - sx
		elif sliding:
			cx = cx+dx
			dx = 0
			sliding = False
			hold_time = time()-b1_begin
			if last_hold < 0.5 and last_up < 0.5 and hold_time < 0.5:
				cur_img += 1
				if cur_img == len(pyimgs):
					cur_img = 0
			last_hold = hold_time
			b0_begin = time()

		main_surface.blit(pyimgs[cur_img], (cx+dx,10))

		write_text("B1:"+str(b1)+"  B2:"+str(b2) + "   B3:"+str(b3), 10, 30, main_surface, font)
		write_text("MX:"+str(mx)+"  MY:"+str(my), 10, 50, main_surface, font)
		write_text("Last Hold:"+str(last_hold)+"  MY:"+str(my), 10, 70, main_surface, font)

		pygame.display.update()
	
		old_b1 = b1

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return 0
if __name__ == '__main__':
	run()