import pygame
from time import sleep
from random import choice
from math import ceil

def tran_none(mainSurface, blitdata):
	mainSurface.fill((0, 0, 0))
	mainSurface.blit(blitdata[0], blitdata[1])
	pygame.display.update()
	return mainSurface

def tran_superimposition(mainSurface, blitdata):
	origionalSurface = mainSurface.copy()
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	for alpha in range(128):
		mainSurface.blit(origionalSurface, (0,0))
		templateSurface.set_alpha(min(255,alpha*4))
		mainSurface.blit(templateSurface, (0,0))
		pygame.display.update()
		sleep(0.001)
	return mainSurface
	
def tran_hblinds(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	sectionWidth = int(ceil(mainSurface.get_width() / 12.0))
	for part in range(sectionWidth):
		for section in range(12):
			line = (sectionWidth * section) + part
			if not line > mainSurface.get_width():
				mainSurface.blit(templateSurface, (line,0), (line,0,1,mainSurface.get_height()))
		pygame.display.update()
		sleep(1.0 / sectionWidth)
	return mainSurface
	
def tran_vblinds(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	sectionHeight = int(ceil(mainSurface.get_height() / 12.0))
	for part in range(sectionHeight):
		for section in range(12):
			line = (sectionHeight * section) + part
			if not line > mainSurface.get_height():
				mainSurface.blit(templateSurface, (0,line), (0,line,mainSurface.get_width(),1))
		pygame.display.update()
		sleep(1.0 / sectionHeight)
	return mainSurface
	
def tran_hwipe(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	for line in range(mainSurface.get_width()):
		mainSurface.blit(templateSurface, (line,0), (line,0,1,mainSurface.get_height()))
		if line % 3 == 0 or line == mainSurface.get_width() - 1:
			pygame.display.update()
			sleep(3.0 / mainSurface.get_width())
	return mainSurface
	
def tran_vwipe(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	for line in range(mainSurface.get_height()):
		mainSurface.blit(templateSurface, (0,line), (0,line,mainSurface.get_width(),1))
		if line % 3 == 0 or line == mainSurface.get_height() - 1:
			pygame.display.update()
			sleep(3.0 / mainSurface.get_height())
	return mainSurface

def tran_disolve(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	sections = []
	for sectionW in range(50):
		for sectionH in range(50):
			sections.append((sectionW, sectionH)) 
	i = 0
	sectionWidth = int(ceil(mainSurface.get_width() / 50.0))
	sectionHeight = int(ceil(mainSurface.get_height() / 50.0))
	while sections != []:
		section = choice(sections)
		sections.remove(section)
		sectionW = section[0] * sectionWidth
		sectionH = section[1] * sectionHeight
		mainSurface.blit(templateSurface, (sectionW,sectionH), (sectionW,sectionH,sectionWidth,sectionHeight))
		i += 1
		if i >= 10:
			pygame.display.update()
			i = 0
			sleep(0.004)
	pygame.display.update()
	return mainSurface

def tran_fade(mainSurface, blitdata):
	origionalSurface = mainSurface.copy()
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	for alpha in range(64):
		mainSurface.blit(origionalSurface, (0,0))
		templateSurface.set_alpha(alpha*4)
		mainSurface.blit(templateSurface, (0,0))
		pygame.display.update()
		sleep(0.005)
	origionalSurface = mainSurface.copy()
	for alpha in range(64):
		mainSurface.blit(origionalSurface, (0,0))
		blitdata[0].set_alpha(alpha*4)
		mainSurface.blit(blitdata[0], blitdata[1])
		pygame.display.update()
		sleep(0.005)
	return mainSurface
	
def tran_boxout(mainSurface, blitdata):
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	halfWidth = ceil(mainSurface.get_width() / 2.0)
	halfHeight = ceil(mainSurface.get_height() / 2.0)
	sectionWidth = halfWidth / 100.0
	sectionHeight = halfHeight / 100.0
	for section in range(1, 101):
		x = halfWidth - ceil(section * sectionWidth)
		y = halfHeight - ceil(section * sectionHeight)
		width = sectionWidth * section * 2
		height = sectionHeight * section * 2
		mainSurface.blit(templateSurface, (x,y), (x,y,width,height))
		pygame.display.update()
		sleep(0.01)
	return mainSurface
	
def tran_boxin(mainSurface, blitdata):
	origionalSurface = mainSurface.copy()
	templateSurface = pygame.Surface(mainSurface.get_size())
	templateSurface.fill((0, 0, 0))
	templateSurface.blit(blitdata[0], blitdata[1])
	halfWidth = ceil(mainSurface.get_width() / 2.0)
	halfHeight = ceil(mainSurface.get_height() / 2.0)
	sectionWidth = halfWidth / 100.0
	sectionHeight = halfHeight / 100.0
	for section in range(1, 101):
		mainSurface.blit(templateSurface, (0,0))
		section = 100 - section
		x = halfWidth - ceil(section * sectionWidth)
		y = halfHeight - ceil(section * sectionHeight)
		width = sectionWidth * section * 2
		height = sectionHeight * section * 2
		mainSurface.blit(origionalSurface, (x,y), (x,y,width,height))
		pygame.display.update()
		sleep(0.01)
	return mainSurface

def tran_random(mainSurface, blitdata):
	choices = transitions.keys()
	choices.remove('Random')
	return transitions[choice(choices)](mainSurface, blitdata)

transitions = {
	'None':               tran_none,
	'Superimposition':    tran_superimposition,
	'Horizontal Blinds':  tran_hblinds,
	'Vertical Blinds':    tran_vblinds,
	'Horizontal Wipe':    tran_hwipe,
	'Vertical Wipe':      tran_vwipe,
	'Disolve':            tran_disolve,
	'Fade':               tran_fade,
	'Box Out':            tran_boxout,
	'Box In':             tran_boxin,
	'Random':             tran_random}
