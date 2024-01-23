# Séance 1 du 05/12/2023
# Prise en main de Pyglet : création d'une fenêtre, détection d'une touche pressée/relâchée

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
from pyglet import shapes
from math import cos, sin

global x_joueur, y_joueur, angle_joueur_horizontal, sensi_horizontale
fenetre2D_largeur = 640
fenetre2D_hauteur = 400
x_joueur = fenetre2D_largeur // 2
y_joueur = fenetre2D_hauteur // 2
angle_joueur_horizontal = 0
sensi_horizontale = 0.02

# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(640, 400, "Plan 2D", vsync=False)

# creating a batch object
joueur = pg.graphics.Batch()

# détection d'un mouvement de la souris
@window2d.event
def on_mouse_motion(x, y, dx, dy):
    global x_joueur, y_joueur, angle_joueur_horizontal
    print("Souris x, y, dx, dy :", "\t", x, "\t", y, "\t", dx, "\t", dy)
    angle_joueur_horizontal += sensi_horizontale*dx

# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
  global x_joueur, y_joueur, angle_joueur_horizontal

  print("Touche pressée n°", symbol)
  # Touche echap : on quitte le jeu  
  if symbol == 65307: pg.app.exit()
  
  if symbol == pg.window.key.Z or symbol == pg.window.key.UP: #haut
      y_joueur += 10

  if symbol == pg.window.key.S or symbol == pg.window.key.DOWN: #bas
      y_joueur -= 10

  if symbol == pg.window.key.Q or symbol == pg.window.key.LEFT: #gauche
      x_joueur -= 10

  if symbol == pg.window.key.D or symbol == pg.window.key.RIGHT: #droite
      x_joueur += 10

'''
  if symbol == pg.window.key.UP or symbol == pg.window.key.LEFT: #fleche haut
       angle_joueur_horizontal += 0.5
       
  if symbol == pg.window.key.DOWN or symbol == pg.window.key.RIGHT: #fleche haut
       angle_joueur_horizontal -= 0.5
'''
       
# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    print("Touche relâchée n°", symbol)

# évènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()
    cercle = shapes.Circle(x_joueur, y_joueur, radius=20, color=(50, 225, 30), batch = joueur)
    line = shapes.Line(x_joueur, y_joueur, x_joueur + 100*cos(angle_joueur_horizontal), y_joueur+100*sin(angle_joueur_horizontal), width=8, batch=joueur)
    joueur.draw()

# lancement du jeu
pg.app.run()
