# Séance 1 du 05/12/2023
# Prise en main de Pyglet : création d'une fenêtre, détection d'une touche pressée/relâchée

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
from pyglet import shapes
from math import cos, sin, pi
from random import randint

# Configuration des commandes
cmd = {"forward":    [pg.window.key.UP , pg.window.key.Z], #vers l'avant : Z ou haut
       "backward":  [pg.window.key.DOWN , pg.window.key.S], #vers l'arrière : S ou bas
       "straf_left":  [pg.window.key.LEFT , pg.window.key.Q], #déplacement latéral gauche : Q ou gauche
       "straf_right": [pg.window.key.RIGHT , pg.window.key.D], #déplacement latéral droite : D ou droite
       "reload":[pg.window.key.R, 65456],  #recharger : R ou Touche 0 du pad num
       "use":[pg.window.key.E, 65457], # utiliser : E ou Touche 1 du pad num
       "walk":  [65505 , 65506], #Marcher : Touche MAJG ou MAJD
       "jump":  [32 , 65508], #Sauter : SPACE ou CTRLD
       "fire":  [pg.window.mouse.LEFT]
       }

global x_joueur, y_joueur, angle_joueur, sensi_horizontale, vitesse
fenetre2D_largeur = 640
fenetre2D_hauteur = 400
x_joueur = fenetre2D_largeur // 2
y_joueur = fenetre2D_hauteur // 2
angle_joueur = 0 # Angle de déplacement
sensi_horizontale = 0.01
vitesse = 25

# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(640, 400, "Plan 2D", vsync=False)

# A retirer quand on aura la fenêtre 3D:
# mettre "mouse exclusive mode" pour masquer le curseur de la souris
# voir https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html#mouse-exclusivity
window2d.set_exclusive_mouse(True)


# creating a batch object
joueur = pg.graphics.Batch()

# détection d'un mouvement de la souris
@window2d.event
def on_mouse_motion(x, y, dx, dy):
    global x_joueur, y_joueur, angle_joueur
    print("Souris x, y, dx, dy :", "\t", x, "\t", y, "\t", dx, "\t", dy)
    angle_joueur += sensi_horizontale*dx
    print("Angle joueur : ", angle_joueur)
    
    angle_joueur = angle_joueur % (2*pi) # angle compris entre 0 et 2pi

# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
  global x_joueur, y_joueur, angle_joueur, vitesse

  print("Touche pressée n°", symbol)

  if symbol == 65307: pg.app.exit() # Echap pour quitter
  
  if symbol in cmd["forward"]: #haut
      x_joueur += vitesse * cos(angle_joueur)
      y_joueur += vitesse * sin(angle_joueur)

  if symbol in cmd["backward"]: #bas
      x_joueur -= vitesse * cos(angle_joueur)
      y_joueur -= vitesse * sin(angle_joueur)

  if symbol in cmd["straf_left"]: #gauche
      x_joueur -= vitesse * sin(angle_joueur)
      y_joueur += vitesse * cos(angle_joueur)

  if symbol in cmd["straf_right"]: #droite
      x_joueur += vitesse * sin(angle_joueur)
      y_joueur -= vitesse * cos(angle_joueur)

  if symbol in cmd["reload"]: #recharger
      print("Rechargement arme")

  if symbol in cmd["use"]: #marcher au lieu de courir
      # Diminuer vitesse d'avance du joueur
      print("Utiliser")

  if symbol in cmd["walk"]: #marcher au lieu de courir
      # Diminuer vitesse d'avance du joueur
      vitesse /= 2.5
      print("Marcher")

  if symbol in cmd["jump"]: #saut
      #Sauter !
      print("Sauter")
      pass

  if symbol in cmd["fire"]: #Tir principal
      #Tirer
      print("Tir")
      pass
'''
  if symbol == pg.window.key.UP or symbol == pg.window.key.LEFT: #fleche haut
       angle_joueur_horizontal += 0.5
       
  if symbol == pg.window.key.DOWN or symbol == pg.window.key.RIGHT: #fleche haut
       angle_joueur_horizontal -= 0.5
'''
       
# détection d'une touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    global vitesse

    print("Touche relâchée n°", symbol)

    if symbol in cmd["walk"]: #Cesser de marcher et re-courir
      vitesse *= 2.5
      print("Courir")

# évènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()
    cercle = shapes.Circle(x_joueur, y_joueur, radius=20, color=(50, 225, 30), batch = joueur)
    line = shapes.Line(x_joueur, y_joueur, x_joueur + 100*cos(angle_joueur), y_joueur+100*sin(angle_joueur), width=7, batch=joueur)
    joueur.draw()

# lancement du jeu
pg.app.run(1/60)  # 60Hz

print("Programme terminé")
