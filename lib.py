import pyglet

class Mur:
    def __init__(self, x, y, largeur, longueur, hauteur = 2, orientation = 0):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.longueur = longueur
        self.hauteur = hauteur
        self.orientation = orientation # en degré

        image = pyglet.image.SolidColorImagePattern((27,35,81,255)).create_image(self.largeur, self.longueur)
        # image.anchor_x = self.largeur // 2
        # image.anchor_y = self.longueur // 2

        self.sprite = pyglet.sprite.Sprite(image, x, y)

    def dessiner(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = -self.orientation
        self.sprite.draw()

