import pygame
from random import randint
from couleur import *

class Screen:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screenSize = self.screen.get_size()
		self.screenWidth = self.screenSize[0]
		self.screenHeight = self.screenSize[1]


class Balle(Screen):
	""" Balle de base. On doit les prendre mais elle ne font rien de particulier """
	def __init__(self, path_ball='img/ball.png'):
		Screen.__init__(self)
		self.typeBall = 'base'
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

class Vaisseau(Screen):
	def __init__(self):
		Screen.__init__(self)
		self.vaisseau = pygame.image.load(path_vaisseau).convert_alpha()
		self.vRect = self.vaisseau.get_rect()

		self.speed = [5, 5]
		# pour qu'il ne soir pas bloquer
		self.vRect = self.vRect.move(self.speed)

		self.score = 0
		self.vie = 0

	def move(self, kgp):
		""" kgp : pygame.key.get_pressed()"""
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

			# on le remet aux positions enregistrees (sinon, il se remet a (0, 0))
			self.vRect = self.vRect.move(pos)

		except pygame.error: # loading error
			print 'Erreur : Chargement de l image', path, 'impossible.'

	def ajoutScore(self, score):
		""" score peut etre negatif """
		self.score += score

	def getScore(self):
		return self.score

	def getVie(self):
		""" Cette methode sert a savoir la vie du vaisseau. Si il a pris un boule bleu, il a une vie. Donc avec son extension, si il se tape une balle noir, il la perd, mais s il est "tout nu", alors il meurt (game over) """
		return self.vie


class Niveau(Screen):
	def __init__(self):
		# ------------------------------------------------------------------------------------- #
		# ------------------------------------ Les niveaux ------------------------------------ #
		# ------------------------------------------------------------------------------------- #
		Screen.__init__(self)
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



class Texte(Screen):
	def __init__(self, font='font/consolas.ttf', size=50):
		Screen.__init__(self)
		self.SIZE = size
		try:
			self.FONT = pygame.font.Font(font, size) # font par defaut
		except pygame.error:
			print 'Impossible de charger', font, '\nPolice par defaut : Consolas'
			self.FONT = pygame.font.Font('font/consolas.ttf', size) # font par defaut

	def center(self, surface, centerx=True, centery=True, xajout=0, yajout=0):
		""" xajout ou yajout peut etre negatif """
		if centerx and centery:
			return surface.get_rect(centerx=self.screen.get_width() / 2 + xajout, centery=self.screen.get_height() / 2 + yajout)
		if centerx:
			return surface.get_rect(centerx=self.screen.get_width() / 2 + xajout)

		if centery:
			return surface.get_rect(centery=self.screen.get_width() / 2 + xajout)


	def render(self, text, font='d', size='d', color=black, surfBlit='d'):
		""" Cette fonction rajoute juste a pygame.font.Font().render() la comprension des \n
			Elle centrera automatiquement verticalement et horizontalement.
		"""
		if font == 'd':
			font = self.FONT
		if size == 'd':
			size = self.SIZE
		if surfBlit == 'd':
			surfBlit = self.screen

		ligne = text.split('\n')
			
		yajout = -25 * (len(ligne) - 1)
		for li in ligne:
			textSurface = font.render(li, True, color)
			rect = textSurface.get_rect(centerx=surfBlit.get_width() / 2, centery=surfBlit.get_height() / 2 + yajout)
			surfBlit.blit(textSurface, rect)
			yajout += 50

	def UTPC(self):
		""" Une touche pour continuer :D """
		texte = self.FONT.render('Une touche pour continuer', 1, gris)
		rect = texte.get_rect()
		x = self.screenSize[0] / 2 - texte.get_width() / 2
		y = self.screenSize[1] - texte.get_height()
		# rect.move()
		self.screen.blit(texte, (x, y))


	def messageJeu(self, titre, message, colorTitre=bleu):
		# titre du message : souligne, couleur user
		self.FONT.set_underline(True)
		titre = self.FONT.render(str(titre), True, colorTitre)
		self.FONT.set_underline(False)

		# message : noir
		# self.screen.fill(-1)

		message = self.render(str(message)) # fonction de cette classe (il se blit tout seul)
		self.screen.blit(titre, (self.center(titre, centery=False)))
		self.UTPC()
		pygame.display.flip()