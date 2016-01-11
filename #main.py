print '======================================== RESTART ========================================'

import pygame
import time
import random as r
from pygame.locals import *
from classes import Balle, Vaisseau, Niveau, CheckContact, BallMakeBigger, BallGiveTime, BallMakeLose, Tools
from couleur import *

pygame.init()

mf = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption('Catch it !')

font = pygame.font.Font('font/consolas.ttf', 40)

niveau_suivant = pygame.mixer.Sound('son/niveau-suivant.wav')
niveau_perdu   = pygame.mixer.Sound('son/niveau-perdu.wav')

tools = Tools()

# -------------------------------------------------------------------------------------------- #
# ------------------------------------------ Niveau ------------------------------------------ #
# -------------------------------------------------------------------------------------------- #

niveau = Niveau()
numNiveau = 1
listBall, parametre = niveau.getNiveau(numNiveau)


def initBall(times):
	""" Init ball nul ! """
	listBall = []
	for i in range(0, times):
		listBall.append(Balle())
	listBall.append(BallMakeBigger())
	listBall.append(BallGiveTime())
	listBall.append(BallMakeLose())
	return listBall


theme = parametre[0] # cette variable n est pas encore effective

# temps de base (en secondes) 
# Attention, le temps que le programme demarre, 0-5 seconde peuvent etre perdu
tempsEnPlus = parametre[1]

# temps que la balle verte (ou horloge) rapporte (en seconde)
tempsRapporteBalleHorloge = parametre[2]


vais = Vaisseau()

t1 = time.time() + tempsEnPlus
time.sleep(1)
clock = pygame.time.Clock()

cont = True
while cont:
	t2 = int(t1 - time.time())

	mf.fill(blanc)
	for e in pygame.event.get():
		if e.type == QUIT:
			cont = False

		if e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				cont = False

			if e.key == K_RETURN:
				t1 += 50

	CC = CheckContact(listBall, vais)
	kgp = pygame.key.get_pressed()
	vais.move(kgp)
	vais.affiche()

	check = CC.checkContact()
	# ------------------------------------------------------------------------------------------ #
	# ------------------------------ Plus de temps donc on arrete ------------------------------ #
	# ------------------------------------------------------------------------------------------ #
	
	if t2 <= 0:
		t2 = 0
		niveau_perdu.play()
		vais.empecheAffiche()
		tools.UTPC()

		texte1 = font.render('Le jeu est fini ! Votre score est de ' + str(vais.getScore()), 1, noir)
		texte2 = font.render('Retour au niveau 0', 1, noir)
		mf.blit(texte1, tools.center(texte1, yajout=-25))
		mf.blit(texte2, tools.center(texte2, yajout=25))

		pygame.display.flip()
		
		pygame.time.delay(2000)
		tools.waitForKeydown()

		check = None
		numNiveau = 1

		listBall, parametre = niveau.getNiveau(numNiveau)
		theme = parametre[0]
		tempsEnPlus = parametre[1]

		tempsRapporteBalleHorloge = parametre[2]

		t1 = time.time() + tempsEnPlus
		vais.reset()

	# ---------------------------------------------------------------------------------------- #
	# ------------------- On ajoute du temps si on a pris une ball horloge ------------------- #
	# ---------------------------------------------------------------------------------------- #
	
	if check == 'ajoutTemps':
		t1 += tempsRapporteBalleHorloge

	# ----------------------------------------------------------------------------------------- #
	# --------------------------- On arrette s il n y plus de balle --------------------------- #
	# ----------------------------------------------------------------------------------------- #
	
	elif check == 'plusDeBalle':

		vais.empecheAffiche()

		texte1 = font.render('Vous passez de niveau !', True, vert)
		texte2 =  font.render('Il vous reste maintenant ' + str(t2) + ' secondes', 1, noir)
		texte3 = font.render('Votre score est de ' + str(vais.getScore()), 1, noir)
		tools.UTPC()
		mf.blit(texte1, tools.center(texte1, yajout=-50))
		mf.blit(texte2, tools.center(texte2, yajout=0))
		mf.blit(texte3, tools.center(texte3, yajout=50))
		delay = 100

		niveau_suivant.play()

		pygame.display.flip()
		pygame.time.delay(2000)
		# pour ne pas qu on appuie directement sur une touche (on appuie sur le fleche a ce moment la) C est le temps minimal de l affichage du message. Essayez de le desactiver pour voir.
		
		clock.tick()
		tools.waitForKeydown()
		clock.tick()
		tempsEcoule = clock.get_time()
		tempsEcoule /= 1000
		t1 += tempsEcoule + 2 # les 2000 ms juste au dessus
		
		check = None
		numNiveau += 1
		listBall, parametre = niveau.getNiveau(numNiveau)
		theme = parametre[0]
		tempsEnPlus = parametre[1]
		tempsRapporteBalleHorloge = parametre[2]
		t1 = time.time() + tempsEnPlus
		vais.reset()

		if listBall == ['End']:
			vais.empecheAffiche()
			mf.fill(-1)
			texte1 = font.render("Fin des niveaux", 1, bleu)
			texte2 = font.render('Il n\'y a pas de niveaux suivants', 1, noir)
			texte3 = font.render('pour le moment.', 1, noir)

			mf.blit(texte1, tools.center(texte1, yajout=-50))
			mf.blit(texte2, tools.center(texte2, yajout=0))
			mf.blit(texte3, tools.center(texte3, yajout=50))
			pygame.display.flip()
			pygame.time.delay(1000)
			tools.waitForKeydown()

			print 'Fin du jeu !'
			cont = False

	# ---------------------------------------------------------------------------------------- #
	# ---------------------------- On arrette si le jeu est perdu ---------------------------- #
	# ---------------------------------------------------------------------------------------- #
	
	elif check == 'jeuEstPerdu':
		vais.empecheAffiche()
		texte1 = font.render('Vous avez perdu !', 1, rouge)
		texte2 = font.render('Vous devez prendre ce type de balle', 1, noir)
		texte3 = font.render('en dernier pour ne pas perdre.', 1, noir)
		tools.UTPC()
		mf.blit(texte1, tools.center(texte1, yajout=-50))
		mf.blit(texte2, tools.center(texte2, yajout=0))
		mf.blit(texte3, tools.center(texte3, yajout=50))
		

		pygame.display.flip()
		pygame.time.delay(2000)
		tools.waitForKeydown()

		vais.reset()

		t1 = time.time() + tempsEnPlus

	if cont == True:
		for i in listBall:
			i.move()
			i.affiche()

	# temps restant (on affiche t2)
	t2 = font.render('temps : ' + str(t2), 1, (150, 150, 150))
	#score joueur
	scoreVaisseau = font.render('score : ' + str(vais.getScore()), 1, (150, 150, 150))

	# vie joueur
	vieVaisseau = font.render('vie : ' + str(vais.getVie()), 1, gris)


	mf.blit(t2, (20, 20))
	mf.blit(scoreVaisseau, (20, 80))
	mf.blit(vieVaisseau, (20, 140))

	pygame.display.flip()
