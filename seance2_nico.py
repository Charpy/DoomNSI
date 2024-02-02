# Séance 1 du 05/12/2023
# Prise en main de Pyglet : création d'une fenêtre, détection d'une touche pressée/relâchée

# module pyglet principal (qu'on renomme en pg pour plus de simplicité)
import pyglet as pg
from pyglet import shapes
from pyglet.window import key
from math import cos, sin, pi
from random import randint
from datetime import datetime  # Juste pour quelques tests
from lib import *


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

# Configuration des variables

fenetre2D_largeur = 640
fenetre2D_hauteur = 400
sensi_horizontale = 0.01
vitesse_max = 0.15 #0.15
mute = False

# Joueurs, à partir d'ici ne plus rien configurer !
x_joueur = fenetre2D_largeur // 2
y_joueur = fenetre2D_hauteur // 2
coord = f"{x_joueur} , {y_joueur}"

angle_joueur = pi/2 # Angle  initial en rad (0 = vers la droite)
vitesse = vitesse_max


#Statistiques : compteurs de touches pressés (press, release), de frames dessinées (draw) et de boucle d'actualisation (loopnumber)
press, release, draw, loopnumber, last_loopnumber = 0, 0, 0, 0, 0




# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(640, 400, "Plan 2D", vsync=False , resizable=True)
# A retirer quand on aura la fenêtre 3D:
# mettre "mouse exclusive mode" pour masquer le curseur de la souris
# voir https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html#mouse-exclusivity
#window2d.set_exclusive_mouse(True)

# Initialisation de KeyStateHandler et lien à la fenêtre
# KeyStateHandler traque l'état des touches du clavier
keys = key.KeyStateHandler()
window2d.push_handlers(keys)

# Groupes d'objets à dessiner
joueur = pg.graphics.Batch() #visuel du joueur et effets spéciaux
gui = pg.graphics.Batch() # interface joueur
carte = pg.graphics.Batch() # dessin 2D de la map

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

arrierePlan = pg.image.SolidColorImagePattern((181,181,181,255)).create_image(fenetre2D_largeur, fenetre2D_hauteur)


murs = []
#Bordure de la carte, par précaution..
murs.append(Mur(x = 5, y = 5, largeur = window2d.width-10, longueur = 10, hauteur = 2, orientation = 0))  # bordure bas
murs.append(Mur(x = 5, y = window2d.height-30, largeur = window2d.width-10, longueur = 10, hauteur = 2, orientation = 0))  # bordure haut
murs.append(Mur(x = 5, y = 5, largeur = 10, longueur = window2d.height-30, hauteur = 2, orientation = 0))  # bordure gauche
murs.append(Mur(x = window2d.width-15, y = 5, largeur = 10, longueur = window2d.height-30, hauteur = 2, orientation = 0))  # bordure droite

#Carte partielle du niveau 1 du Doom original
# voir https://www.classicdoom.com/maps/d1maps/e1m1.htm

piece_de_spawn = [
                (230,39),
(258,39),
(258,25),
(288,25),
(288,39),
(316,39),
(374,81),
(402,81),
(402,383),
(232,383),
(174,353),
(116,353),
(116,283),
(30,267),
(30,183),
(116,167),
(116,81),
(174,81)
                ]
spawn = pg.shapes.Polygon(*piece_de_spawn, color = (27,35,81,255), batch = carte)



# Création des sprites, ce sont des instances 
# des images, affichés à l'écran
player_sprite = pg.sprite.Sprite(player_image, x_joueur, y_joueur, batch=joueur)
player_sprite.rotation = -angle_joueur*180/pi #Orientation initiale du sprite, en deg (haut)

# Initialisation de la musique d'ambiance
# Bonnes musiques d'ambiance libres : https://incompetech.com/music/royalty-free/music.html
liste_ambiance = ['Brain Dance.mp3', 'Galactic Rap.mp3', 'Lord of the Rangs.mp3', 'Cloud Dancer.mp3', 'Karstenholymoly_-_The_Invisible_Enemy_(feat._bangcorrupt).mp3', 'SCP-x2x_horror.mp3']
ambiance = pg.resource.media(liste_ambiance[randint(0,len(liste_ambiance)-1)])
gunfire = pg.resource.media('beretta m12 9 mm.mp3', streaming=False) # streaming=False pour les bruitages rapides! voir https://pyglet.readthedocs.io/en/latest/programming_guide/quickstart.html#playing-sounds-and-music
gunreload = pg.resource.media('Pistolet-reload.mp3', streaming=False)

# etatSons = {} #Etat d'un son (non joué / joué), utile pour certains sons qui ne doivent pas s'auto-chevaucher
if not mute : ambiance.play()


#Chargement des infos sur la fenêtre
coord_label = pg.text.Label(coord, x=5, y=window2d.height - 15, color=(27,35,81,255), batch=gui)
titre2D_label = pg.text.Label(text="Vue 2D", x=window2d.width//2, y=window2d.height - 15, color=(27,35,81,255), anchor_x='center', batch=gui)

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
      if not mute: gunfire.play()
    
    if button in cmd["zoom"]: #Zoom de l'arme en main
      #Zoom
      print("Zoom")

# Détection d'un redimensionnement de la fenêtre par l'utilisateur
# On recalcule les positions de l'interface
@window2d.event
def on_resize(width, height):
    global titre2D_label, coord_label, arrierePlan
    print("on_resize a été appelé")
    coord_label.x = 5
    coord_label.y = height - 15
    titre2D_label.x = width // 2
    titre2D_label.y = height - 15
    
    #On redessine l'arrière-plan
    arrierePlan = pg.image.SolidColorImagePattern((181,181,181,255)).create_image(width, height)
# @window2d.event
# def on_draw():
#     global draw, last_loopnumber, loopnumber
#     draw += 1
#     # print(loopnumber-last_loopnumber,"loops since last draw")
#     # last_loopnumber = loopnumber
#     # print("on_draw", draw)
#     window2d.clear()

#Test si une des touches d'une action est active
def est_pressee(touches):
    global keys
    return True in list(map(lambda x:keys[x]==True , touches))
# def est_pressee(touches):
#     print("touches",touches)
#     for touche in touches:
#     return True in list(map(lambda x:keys[x]==True , touches))

# Evènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()

    arrierePlan.blit(0,0) #arrière plan

    # cercle = shapes.Circle(x_joueur, y_joueur, radius=20, color=(50, 225, 30), batch = joueur)    


    
    coord_label.draw()

    titre2D_label.draw()

    joueur.draw()

    # test.dessiner()
    # for mur in murs:
    #     mur.dessiner()

    spawn.draw()
    # shapes.Circle(x=230, y=44, radius=5, color=(255,255,255,255)).draw()

    joueur.draw()
    # print("refresh!")
    # print(datetime.now())



@window2d.event
def on_key_press(symbol, modifiers):
    global press
    press += 1

    print("key press", symbol)

    window2d.push_handlers(keys) #Récupére l'état des touches (bool)


    # Touches d'actions discontinues (une seule exécution en maintenant la touche)

    if symbol in cmd.get("reload"): #Recharger
        print("Play son gunreload")
        if not mute : gunreload.play()
        print("Rechargement arme")

    if est_pressee(cmd["use"]): #Utiliser objet
        print("Utiliser")

    if est_pressee(cmd["jump"]): #saut
        #Sauter !
        print("Sauter")
        pass

@window2d.event
def on_key_release(symbol, modifiers):
    global release
    release += 1
    print("key release", symbol)



    # print("\t\t\t\t\t\t\t\ton_key_release", release)

@window2d.event
def update(dt):
    global loopnumber
    loopnumber += 1
    # print("on_loop", loopnumber)

    global x_joueur, y_joueur, angle_joueur, vitesse, coord
    # print(datetime.now())  #Vérif fréquence
    # if keys[key.ESCAPE]: pg.app.exit() # Echap pour quitter
    # if keys[key.UP] or keys[key.Z]:  # Haut

    # Touches d'actions continues (Poursuivre l'exécution en maintenant la touche)

    if keys[key.ESCAPE]: pg.app.exit() # Echap pour quitter

    if est_pressee(cmd["forward"]):  # Haut
        x_joueur += vitesse * cos(angle_joueur)
        y_joueur += vitesse * sin(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if est_pressee(cmd["backward"]):  # Bas
        x_joueur -= 0.75 * vitesse * cos(angle_joueur)
        y_joueur -= 0.75 * vitesse * sin(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if est_pressee(cmd["straf_left"]):  # Gauche
        x_joueur -= 0.9 * vitesse * sin(angle_joueur)
        y_joueur += 0.9 * vitesse * cos(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if est_pressee(cmd["straf_right"]):  # Droite
        x_joueur += 0.9 * vitesse * sin(angle_joueur)
        y_joueur -= 0.9 * vitesse * cos(angle_joueur)
        coord = f"{round(x_joueur)}, {round(y_joueur)}"

    if est_pressee(cmd["walk"]): #marcher au lieu de courir
        # Diminuer vitesse d'avance du joueur
        vitesse = vitesse_max / 2
        print("vitesse :", vitesse)
        print("Marcher")
    else:
        # to-do : mettre cette partie dans key_release
        vitesse = vitesse_max
        print("vitesse :", vitesse)

    
    #Maj des élements a afficher
    player_sprite.x = x_joueur
    player_sprite.y = y_joueur
    coord_label.text = coord
    ligne_du_regard = shapes.Line(x_joueur, y_joueur, x_joueur + 100*cos(angle_joueur), y_joueur+100*sin(angle_joueur), width = 7, color = (255, 255, 255, 100), batch = joueur)

















# Configuration de la fonction de mise à jour avec functools.partial
# pg.clock.schedule_interval(update, 1/20)
# lancement du jeu
# pg.clock.schedule(on_key_press) #test
pg.clock.schedule(update)

# pg.clock.set_fps_limit(60)  # Réglez la fréquence de rafraîchissement à 60 FPS

if __name__ == '__main__':
    pg.app.run(1/120)
# pg.app.run()  # 60Hz par défaut
# pg.app.run(1/120)

print("----------------")
print("Programme terminé")
print("----------------")
print("on_draw", draw)
print("on_key_release", release)
print("key press", press)
print("on_loop", loopnumber)
