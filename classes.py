

import pygame
from pygame.locals import *
from constantes import *

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier, demon = True):
		self.fichier = fichier
		self.structure = 0
		self.demon = demon

	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau


	def afficher(self, fenetre):
		arrivee = pygame.image.load(image_arrivee).convert_alpha()
		depart = pygame.image.load(image_depart).convert()
		if self.demon:
			mur = pygame.image.load(image_Mdemon).convert_alpha()
		else:
			mur = pygame.image.load(image_mur).convert_alpha()

		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == 'd':		   #d = Départ
					fenetre.blit(depart, (x,y))
				elif sprite == 'a':		   #a = Arrivée
					fenetre.blit(arrivee, (x,y))
				num_case += 1
			num_ligne += 1

class Perso:
	def __init__(self, droite, gauche, haut, bas, niveau, ciel):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		self.ciel = pygame.image.load(haut).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau


	def teleporter(self, nouveau_niveau, x = 0, y = 0, case_x = 0, case_y = 0):
		self.niveau = nouveau_niveau
		self.case_x = case_x
		self.case_y = case_y
		self.x = x
		self.y = y


	def retour(self):
		self.teleporter(self.niveau)


	def deplacer(self, direction):
			#Déplacement vers la droite
		print("direction "+direction)
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			print("x ",self.case_x)
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.droite

		#Déplacement vers la gauche
		if direction == 'gauche':
			print("x ",self.case_x)
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.gauche

		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.haut

		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.bas

		if direction == 'ciel':
			if self.case_y > 0:
					self.case_y -= 2
					self.y = self.case_y * taille_sprite
			self.direction = self.haut



class Monstre(Perso):
	def __init__(self, droite, gauche, haut, bas, niveau, ciel):
		super(Monstre, self).__init__(droite, gauche, haut, bas, niveau, ciel)

		self.poid = 0.1
		self.vie = 10

	def graviter(self):
		return Graviter ()

class Hero(Perso):
	def __init__(self, droite, gauche, haut, bas, niveau, nom, ciel,):
		super(Hero, self).__init__(droite, gauche, haut, bas, niveau, ciel,)

		self.nom = nom
		self.vie = 5

	def pouvoir(self):
		return Pouvoir(image_pouvoir, 4, self.direction, self.x, self.y,
		self.case_x, self.case_y, self.gauche, self.droite)


class Pouvoir():

	def __init__(self, image, distance, direction, x, y, case_x, case_y, droite , gauche):
		self.image = image
		self.distance = distance
		self.direction = direction
		self.case_x = case_x
		self.case_y = case_y
		self.x = x
		self.y = y
		self.droite = droite
		self.gauche = gauche

	def fini(self):
		if self.distance <= 0:
			return True
		else:
			return False

	def pas_fini(self):
		return not self.fini()

	def deplacer (self, direction):
		if direction == 'droite':
			if self.case_x < (nombre_sprite_cote - 1):
				self.case_x += 1
				self.x = self.case_x * taille_sprite
			self.direction = self.droite

		if direction == 'gauche':
			if self.case_x > 0:
				self.case_x -= 1
				self.x = self.case_x * taille_sprite
			self.direction = self.gauche

		self.distance -= 1

class Graviter():
	def _init_ (self, poid, personnage):
		self.poid = 1,8
		self.personnage = Monstre
