# touchscreen_diagnostic.py
# Written by Samwell Freeman
# LucidTronix, June 2016

import pygame
import pygame.ftfont

def write_text(text, x, y, surface, font, size=1, color=(255,255,255)):
	label = font.render(text, size, color)
	surface.blit(label, (x, y))


def run(fullscreen=False):
	pygame.display.init()
	pygame.ftfont.init()
	font = pygame.ftfont.Font(None, 24)

	if fullscreen:
		resolution = pygame.display.list_modes()[0]
		main_surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
	else:
		main_surface = pygame.display.set_mode((300, 200))

	while True:
		main_surface.fill(0)
		mx, my = pygame.mouse.get_pos()
		write_text("Touch Screen Diagnostics", 10, 10, main_surface, font)
		write_text("MX:"+str(mx)+"  MY:"+str(my), 10, 50, main_surface, font)
		pygame.display.update()
	
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()
				return 0
if __name__ == '__main__':
	run()