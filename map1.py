import pyglet
from lib import *


murs = []
#Bordure de la carte, par précaution..
murs.append(Mur(x = 5, y = 5, largeur = window2d.width-10, longueur = 10, hauteur = 2, orientation = 0))  # bordure bas
murs.append(Mur(x = 5, y = window2d.height-30, largeur = window2d.width-10, longueur = 10, hauteur = 2, orientation = 0))  # bordure haut
murs.append(Mur(x = 5, y = 5, largeur = 10, longueur = window2d.height-30, hauteur = 2, orientation = 0))  # bordure gauche
murs.append(Mur(x = window2d.width-15, y = 5, largeur = 10, longueur = window2d.height-30, hauteur = 2, orientation = 0))  # bordure droite

#Carte partielle du niveau 1 du Doom original
# voir https://www.classicdoom.com/maps/d1maps/e1m1.htm

piece_de_spawn = [
                    (116,86),
                    (174,86),
                    (230,44),
                    (258,44),
                    (258,30),
                    (288,30),
                    (288,44),
                    (316,44),
                    (374,86),
                    (402,86),
                    (402,388),
                    (232,388),
                    (174,358),
                    (116,358),
                    (116,288),
                    (30,272),
                    (30,188),
                    (116,172),
                    (116,86)
                ]
pyglet.shapes.Polygon(piece_de_spawn, color = (27,35,81,255), batch = carte).draw()


