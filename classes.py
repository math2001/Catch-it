import pygame
import re # regex
from pygame.locals import *
from random import randint
from couleur import *
import time

def NoneFonction():
	""" Cette fonction sert a desaciver d autre fonction """
	pass


class Balle:
	""" Balle de base. On doit les prendre mais elle ne font rien de particulier """
	def __init__(self, path_ball='img/ball.png'):
		self.typeBall = 'base'
		self.screen = pygame.display.get_surface()
		self.screenSize = self.screen.get_size()
		self.ball = pygame.image.load(path_ball).convert_alpha()
		self.ballRect = self.ball.get_rect()
		self.speed = [randint(-3, 3), randint(-3, 3)]

		self.ballRect = self.ballRect.move((randint(20, self.screenSize[0] - 20), randint(20, self.screenSize[1] - 20)))		

		# on gagne 1 quand on prend cette balle

		self.score = 1
	def move(self):
		if self.ballRect.left < 0 or self.ballRect.right > self.screenSize[0]:
			self.speed[0] = -self.speed[0]

		if self.ballRect.top < 0 or self.ballRect.bottom > self.screenSize[1]:
			self.speed[1] = -self.speed[1]

		self.ballRect = self.ballRect.move(self.speed)

	def get_rect(self):
		return self.ballRect

	def affiche(self):
		self.screen.blit(self.ball, self.ballRect)

	def getTypeBall(self):
		return self.typeBall

	def getScore(self):
		return self.score

""" Ces classes herite de Balle. """
class BallMakeBigger(Balle):
	"""Lorsqu'on l attrape, votre vaisseau devient plus gros. Voir la class CheckContact"""
	def __init__(self, path='img/blue_ball.png'):
		Balle.__init__(self)
		self.ball = pygame.image.load(path).convert_alpha()
		self.typeBall = 'blue'
		self.score = 0

class BallGiveTime(Balle):
	""" Cette balle rajoute 10 seconde de temps."""
	def __init__(self, path='img/horloge.png'):
		Balle.__init__(self)
		self.ball = pygame.image.load(path).convert_alpha()
		self.typeBall = 'green'
		self.score = 0

class BallMakeLose(Balle):
	""" Cette balle met fin au jeu sauf si on la prend en derniere """
	def __init__(self, path='img/bombe.png'):
		Balle.__init__(self)
		self.ball = pygame.image.load(path).convert_alpha()
		self.typeBall = 'black'
		self.score = 0

class Vaisseau:
	def __init__(self, path_vaisseau='img/vaisseau.png'):
		self.screen = pygame.display.get_surface()
		self.screenSize = self.screen.get_size()
		self.vaisseau = pygame.image.load(path_vaisseau).convert_alpha()
		self.vRect = self.vaisseau.get_rect()

		self.speed = [5, 5]
		self.vRect = self.vRect.move(self.speed)

		self.score = 0
		self.vie = 0

	def move(self, kgp):
		if kgp[K_LEFT] and self.vRect.left > 0:
			self.vRect = self.vRect.move((-self.speed[0], 0))
		if kgp[K_RIGHT] and self.vRect.right < self.screenSize[0]:
			self.vRect = self.vRect.move((self.speed[0], 0))
		if kgp[K_UP] and self.vRect.top > 0:
			self.vRect = self.vRect.move((0, -self.speed[1]))
		if kgp[K_DOWN] and self.vRect.bottom < self.screenSize[1]:
			self.vRect = self.vRect.move((0, self.speed[1]))

	def affiche(self):
		self.screen.blit(self.vaisseau, self.vRect)

	def get_rect(self):
		return self.vRect

	def changeVaisseau(self, path):
		p = re.compile('big')
		m = p.search(path)
		if m:
			self.vie = 1
		else:
			self.vie = 0
		try:
			# on recupere la position de l ancien vaisseau
			pos = self.vRect.x, self.vRect.y

			# on met a jour les variables
			self.vaisseau = pygame.image.load(path).convert_alpha()
			self.vRect = self.vaisseau.get_rect()

			# on le remet au positions enregistrees (sinon, il se remet a (0, 0))
			self.vRect = self.vRect.move(pos)
		except pygame.error:
			print 'Erreur : Chargement de l image', path, 'impossible.'

	def ajoutScore(self, score):
		self.score += score

	def getScore(self):
		return self.score

	def getVie(self):
		""" Cette methode sert a savoir la vie du vaisseau. Si il a pris un boule bleu, il a une vie. Donc avec son extension, si il se tape une balle noir, il la perd, mais s il est "tout nu", alors il meurt (game over) """
		return self.vie

	def ajoutVie(self, nbVieEnPlus):
		""" nbVieEnPlus peut etre negatif """
		self.vie += nbVieEnPlus

	def empecheAffiche(self):
		# self.vRect = self.vRect.move( [-(self.screenSize[0] + 100), -(self.screenSize[1] + 100)] )
		# self.vRect = self.vRect.move( [(self.screenSize[0] + 100), (self.screenSize[1] + 100)] )
		self.vaisseauSave = self.vaisseau.copy()
		self.vaisseau = pygame.Surface((500, 500)) # c est une marge, il faut au minimum que ce soit 75 (taille du plus gros vaisseau pour le moment)
		self.vaisseau.fill(-1)
		self.affiche()

	def reaffiche(self):
		self.vaisseau = self.vaisseauSave

	def reset(self):
		self.vaisseau = pygame.image.load('img/vaisseau.png').convert_alpha()
		self.vRect = self.vaisseau.get_rect()
		self.score = 0
		self.vie = 0

class CheckContact:
	def __init__(self, listBall, vaisseau):
		self.listBall = listBall
		self.vaisseau = vaisseau
		self.SON = {
			'aspire'    : pygame.mixer.Sound('son/aspire.wav'),
			'gonfle'    : pygame.mixer.Sound("son/gonfle.wav"),
			'explosion' : pygame.mixer.Sound("son/explosion.wav")
		}

	def checkContact(self):
		
		ajoutTemps = jeuEstPerdu = False
		plusDeBalle = True # cette variable passe a False si il reste au moins un balle
		for ball in self.listBall:
			plusDeBalle = False
			ballRect = ball.get_rect()
			vaisRect = self.vaisseau.get_rect()
			if vaisRect.colliderect(ballRect):
				# on ajoute le score.
				self.vaisseau.ajoutScore(ball.getScore())

				# on regarde si ce n est pas une balle special
				typeBall = ball.getTypeBall()
				if typeBall == 'blue':
					self.vaisseau.ajoutVie(1)
					self.SON['gonfle'].play()
					self.vaisseau.changeVaisseau('img/big-vaisseau.png')
				elif typeBall == 'green':
					ajoutTemps = True
				elif typeBall == 'black':
					if len(self.listBall) > 1:
						self.SON['explosion'].play()
						if self.vaisseau.getVie() == 1:
							# il perd son extension
							self.vaisseau.changeVaisseau('img/vaisseau.png')
						else:
							jeuEstPerdu = True

				else:
					self.SON['aspire'].play()
					
				self.listBall.remove(ball)

		if ajoutTemps:
			return 'ajoutTemps'
		if jeuEstPerdu:
			return 'jeuEstPerdu'
		if plusDeBalle:
			return 'plusDeBalle'


class Tools:
	def __init__(self, pathFont='font/consolas.ttf', size=40):
		self.screen = pygame.display.get_surface()
		self.screenSize = self.screen.get_size()
		self.font = pygame.font.Font(pathFont, size)

	def center(self, surface, xajout=0, yajout=0):
		""" xajout ou yajout peut etre negatif """
		return surface.get_rect(centerx=self.screen.get_width() / 2 + xajout, centery=self.screen.get_height() / 2 + yajout)

	def waitForKeydown(self):
		""" cette fonction tourne tant qu aucun evenement de type KEYDOWN n est ajoute sur la queue"""
		cont = True
		while cont:
			ev = pygame.event.wait()
			if ev.type == KEYDOWN:
				cont = False

	def UTPC(self):
		""" Une touche pour continuer :D """
		texte = self.font.render('Une touche pour continuer', 1, gris)
		rect = texte.get_rect()
		x = self.screenSize[0] / 2 - texte.get_width() / 2
		y = self.screenSize[1] - texte.get_height()
		# rect.move()
		self.screen.blit(texte, (x, y))


class Niveau:
	def __init__(self):
		# ------------------------------------- #
		# ------------ Les niveaux ------------ #
		# ------------------------------------- #
		
		self.listeNiveau = [
			# plan d un niveau : 
			# [
			# 	theme, temps_de_jeu (en sec), temps_donnee_par_horloge,
			# 	nb_ball_normal, nb_ball_make_bigger, nb_ball_horloge, nb_ball_bombe
			# ]
			# theme peut etre :
			# 	- defaut

			[ # 1 - decouverte balle de base
				'defaut', 20, 0,
				10, 0, 0, 0
			],
			[ # 2 - decouverte balle horloge 
				'defaut', 20, 10,
				30, 0, 2, 0 
			],
			[ # 3 - decouverte balle PLUS GROS
				'defaut', 30, 0,
				10, 1, 0, 0
			],
			[ # 4 - decouverte balle bombe
				'defaut', 30, 0,
				10, 0, 0, 1
			],
			[ # 5 - decouverte balle bombe annule par extension
				'defaut', 30, 0,
				10, 1, 0, 1
			]

		]

	def _verifDifficulte(self, d, maxi=10):
		if d > maxi or d < 0:
			return int(d)
		else:
			return 1
	def generer(self, difficulte=1, normal=True, bombe=True, horloge=True, plusGros=True):
		""" 
			Cette fonction genere un niveau en fonction de difficulte avec les types de balle selectionne.
			difficulte doit etre un int superieur ou egale a 1 et inferieur a 10. Si ce n'est pas le cas, elle sera egale a 1.
			Elle n'est pas bien !
		"""

		r = randint
		maxi = 10
		difficulte = self._verifDifficulte(difficulte, maxi)

		min_normal = 5

		if normal:
			normal = r(0, difficulte * 2 + 2)

			# Cette condition sert a faciliter le developement de cette fonction
			if normal < min_normal:
				normal = min_normal
		else:
			normal = 0

		# BOMBE
		if bombe:
			bombe   = r(0, (difficulte / 2) * 3) # au niveau 1, il n y en aura pas
		else:
			bombe = 0

		# HORLOGE
		if horloge:
			v = difficulte - 5
			if v < 0:
				v = 0 
			horloge = r(0 + (maxi / 4 - difficulte), (maxi - difficulte))
			if horloge < 0:
				horloge = 0
		else:
			horloge = 0

		# PLUS GROS
		if plusGros:
			difficulte -= 1

			plusGros = r(-difficulte, maxi / 3)
			if plusGros < 0:
				plusGros = 0
			if plusGros > 1:
				plusGros = 1
		else:
			plusGros = 0
		
		return normal, bombe, horloge, plusGros

	def getNiveau(self, nb):
		nb -= 1
		try:
			plan = self.listeNiveau[nb]
			parametre = []
			listBall_fonction = []
		except IndexError:
			print 'Impossible de charger ce niveau. nb n\'est pas valide !'
			return ['End'], [0, 0, 0]

		# PARAMETRE
		for i in range(3):
			parametre.append(plan[i])

		# BALLE
		for ball_normal in range(plan[3]):
			listBall_fonction.append(Balle())
		for ball_make_bigger in range(plan[4]):
			listBall_fonction.append(BallMakeBigger())
		for ball_horloge in range(plan[5]):
			listBall_fonction.append(BallGiveTime())
		for ball_bombe in range(plan[6]):
			listBall_fonction.append(BallMakeLose())

		return listBall_fonction, parametre

