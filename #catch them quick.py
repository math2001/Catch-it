# -*- encoding: utf-8 -*-
import pygame as pygame
import random as r
from pygame.locals import *
from classes_update import Texte
from couleur import *

pygame.init()

mf = pygame.display.set_mode((0, 0), FULLSCREEN)


texte = Texte()

cont = True
while cont:
	mf.fill(blanc)
	for e in pygame.event.get():
		if e.type == QUIT:
			cont = False

		if e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				cont = False

	pygame.display.flip()