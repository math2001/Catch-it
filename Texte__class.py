import pygame
from pygame.locals import *
from couleur import *
from classes_update import Screen

class Texte(Screen):
	def __init__(self):
		Screen.__init__(self)
		self.font = pygame.font.Font('font/consolas.ttf', 50)
		self.size = 50

	def _estCeQueCaRentre(self, texte, nbToTest=1):
		""" On test si la partie nbToTest rentre dans l ecran. Les parties sont definis par les \n """
		nbToTest -= 1
		texte.split('|')
		print '_', texte
		tWidth = self.font.size(texte)[0]
		print tWidth
		print self.screenWidth
		if tWidth <= self.screenWidth:
			return True
		else:
			return False
			print 'return FALSE ------- '

	def render(self, texte):
		remplacerEspace = True
		newText = ''
		index = 0
		listeLigne = []
		for i in range(len(texte)):
			caractere = len(texte) - i - 1
			if texte[caractere] == ' ':
				test = self._estCeQueCaRentre(newText)
				if test:
					print 'Ca RENTRE !'
					newText += '@'
					listeLigne.append(newText.split('@')[0])
			else:
				newText += texte[caractere]
		print newText
		print newText.reverse()

"""
Pour chaque caractere:
	si c est un espace:
		on le remplace par un "|"
		on verifie si le texte rentre dans l ecran
		si oui:
			on 
"""