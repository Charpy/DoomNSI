# Séance 1 du 05/12/2023
# Prise en main de Pyglet : création d'une fenêtre, détection d'une touche pressée/relâchée

# module pyglet principal (qu'on renomme en pg pour plus de simplicité)
import pyglet as pg
from pyglet import shapes
from pyglet.window import key
from math import cos, sin, pi
from random import randint
from datetime import datetime  # Juste pour quelques tests

# Configuration des commandes
cmd = {"forward":     [pg.window.key.UP , pg.window.key.Z], #vers l'avant : Z ou haut
       "backward":    [pg.window.key.DOWN , pg.window.key.S], #vers l'arrière : S ou bas
       "straf_left":  [pg.window.key.LEFT , pg.window.key.Q], #déplacement latéral gauche : Q ou gauche
       "straf_right": [pg.window.key.RIGHT , pg.window.key.D], #déplacement latéral droite : D ou droite
       "reload":      [pg.window.key.R, pg.window.key.NUM_0],  #recharger : R ou Touche 0 du pad num
       "use":         [pg.window.key.E, pg.window.key.NUM_1], # utiliser : E ou Touche 1 du pad num
       "walk":        [pg.window.key.LSHIFT , pg.window.key.RSHIFT], #Marcher : Touche MAJG ou MAJD
       "jump":        [pg.window.key.SPACE , pg.window.key.RCTRL], #Sauter : SPACE ou CTRLD
       "fire":        [1], #clic gauche
       "zoom":        [4] #clic droit
       }

fenetre2D_largeur = 640
fenetre2D_hauteur = 400
x_joueur = fenetre2D_largeur // 2
y_joueur = fenetre2D_hauteur // 2
angle_joueur = 0 # Angle  initial en rad (0 = vers la droite)
sensi_horizontale = 0.01
vitesse_max = 4
vitesse = vitesse_max

# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(640, 400, "Plan 2D", vsync=False , resizable=True)
# A retirer quand on aura la fenêtre 3D:
# mettre "mouse exclusive mode" pour masquer le curseur de la souris
# voir https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html#mouse-exclusivity
#window2d.set_exclusive_mouse(True)

# Initialisation de KeyStateHandler et lien à la fenêtre
keys = key.KeyStateHandler()
window2d.push_handlers(keys)

# Groupes d'objets à dessiner
joueur = pg.graphics.Batch()
gui = pg.graphics.Batch() # interface joueur


#Chargement des ressources (images, sons..)
pg.resource.path = ['assets/']
pg.resource.reindex()

# Autres exemples d'images de vues de dessus : https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbrashmonkey.com%2Fforum%2Fuploads%2Fmonthly_2016_03%2Fsample.jpg.9364511bc24a5c41158883fca7523df9.jpg&f=1&nofb=1&ipt=c7af4569ced59c7c7b23231d4762263435fddd8f1309ae58ba908c168a2fed6c&ipo=images
player_image = pg.resource.image("joueur2D.png") #vue de dessus

def centrer_image(image):
    """Positionner l'origine de l'image en son centre"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

centrer_image(player_image)

# Création des sprites, ce sont des instances 
# des images, affichés à l'écran
player_sprite = pg.sprite.Sprite(player_image, x_joueur, y_joueur)


#Chargement des infos sur la fenêtre
coord = str(x_joueur) + "," + str(y_joueur)
coord_label = pg.text.Label(coord, x=5, y=window2d.height - 15)
titre2D_label = pg.text.Label(text="Vue 2D", x=window2d.width//2, y=window2d.height - 15, anchor_x='center')

# détection d'un mouvement de la souris
@window2d.event
def on_mouse_motion(x, y, dx, dy):
    global angle_joueur
    print("Souris x, y, dx, dy :", "\t", x, "\t", y, "\t", dx, "\t", dy)
    angle_joueur += sensi_horizontale*dx
    print("Angle joueur : ", angle_joueur)
    player_sprite.rotation = -angle_joueur*180/pi #angle de rot (en deg)
    
    angle_joueur = angle_joueur % (2*pi) # conserver l'angle entre 0 et 2pi

# détection d'un clic de la souris
@window2d.event
def on_mouse_press(x, y, button, modifiers):
    print("Bouton appuyé et coord :", x, y, button)
    if button in cmd["fire"]: #Tir principal
      #Tirer
      print("Tir")
    
    if button in cmd["zoom"]: #Zoom de l'arme en main
      #Zoom
      print("Zoom")

'''
# détection d'une touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
  global x_joueur, y_joueur, angle_joueur, vitesse, coord

  print("Touche pressée n°", symbol)

  if symbol == pg.window.key.ESCAPE: pg.app.exit() # Echap pour quitter
  
  if symbol in cmd["forward"]: #haut
      x_joueur += vitesse * cos(angle_joueur)
      y_joueur += vitesse * sin(angle_joueur)
      coord = str(round(x_joueur,None)) + "," + str(round(y_joueur,None))

  if symbol in cmd["backward"]: #bas
      x_joueur -= vitesse * cos(angle_joueur)
      y_joueur -= vitesse * sin(angle_joueur)
      coord = str(round(x_joueur,None)) + "," + str(round(y_joueur,None))

  if symbol in cmd["straf_left"]: #gauche
      x_joueur -= vitesse * sin(angle_joueur)
      y_joueur += vitesse * cos(angle_joueur)
      coord = str(round(x_joueur,None)) + "," + str(round(y_joueur,None))

  if symbol in cmd["straf_right"]: #droite
      x_joueur += vitesse * sin(angle_joueur)
      y_joueur -= vitesse * cos(angle_joueur)
      coord = str(round(x_joueur,None)) + "," + str(round(y_joueur,None))

  if symbol in cmd["reload"]: #recharger
      print("Rechargement arme")

  if symbol in cmd["use"]: #Utiliser objet
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


# détection d'une touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    global vitesse
    print("Touche relâchée n°", symbol)
    if symbol in cmd["walk"]: #Cesser de marcher et re-courir
      vitesse *= 2.5
      print("Courir")

'''

@window2d.event
def on_resize(width, height):
    global titre2D_label, coord_label
    print("on_resize a été appelé")
    coord_label = pg.text.Label(coord, x=5, y=height - 15)
    titre2D_label = pg.text.Label(text="Vue 2D", x=width//2, y=height - 15, anchor_x='center') #Au cas où la fenetre ait été redimensionnée

# evènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()

    # cercle = shapes.Circle(x_joueur, y_joueur, radius=20, color=(50, 225, 30), batch = joueur)    
    # player_image.blit(x_joueur, y_joueur)
    player_sprite.x = x_joueur
    player_sprite.y = y_joueur
    player_sprite.draw()

    line = shapes.Line(x_joueur, y_joueur, x_joueur + 100*cos(angle_joueur), y_joueur+100*sin(angle_joueur), width = 7, batch = joueur)
    
    coord_label.text = coord
    coord_label.draw()

    titre2D_label.draw()

    joueur.draw()

    # print("Coucou le refresh!")
    # print(datetime.now())

#Test si une des touches d'une action est active
def press(touches):
    return True in list(map(lambda x:keys[x]==True , touches))

@window2d.event
def update(dt):
    global x_joueur, y_joueur, angle_joueur, vitesse, coord

    # print(datetime.now())  #Vérif fréquence

    # if keys[key.ESCAPE]: pg.app.exit() # Echap pour quitter

    # if keys[key.UP] or keys[key.Z]:  # Haut
    if press(cmd["forward"]):  # Haut
        x_joueur += vitesse * cos(angle_joueur)
        y_joueur += vitesse * sin(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if press(cmd["backward"]):  # Bas
        x_joueur -= 0.75 * vitesse * cos(angle_joueur)
        y_joueur -= 0.75 * vitesse * sin(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if press(cmd["straf_left"]):  # Gauche
        x_joueur -= 0.9 * vitesse * sin(angle_joueur)
        y_joueur += 0.9 * vitesse * cos(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if press(cmd["straf_right"]):  # Droite
        x_joueur += 0.9 * vitesse * sin(angle_joueur)
        y_joueur -= 0.9 * vitesse * cos(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"
    
    if press(cmd["reload"]): #recharger
      print("Rechargement arme")

    if press(cmd["backward"]): #Utiliser objet
      print("Utiliser")

    if press(cmd["walk"]): #marcher au lieu de courir
      # Diminuer vitesse d'avance du joueur
      vitesse = vitesse_max / 2
      print("Marcher")
    else:
       vitesse = vitesse_max

    if press(cmd["jump"]): #saut
      #Sauter !
      print("Sauter")
      pass

    if press(cmd["fire"]): #Tir principal
      #Tirer
      print("Tir")
      pass

# Configuration de la fonction de mise à jour avec functools.partial
pg.clock.schedule_interval(update, 1/60)
# lancement du jeu
# pg.clock.schedule(on_key_press) #test
# pg.app.run()  # 60Hz

# pg.clock.set_fps_limit(60)  # Réglez la fréquence de rafraîchissement à 60 FPS
pg.app.run(1/60)

print("Programme terminé")
