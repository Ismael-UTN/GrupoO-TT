import pygame
import comunes
import math
from Bala import Bala
import random
from Camara import Camara

class Enemigo:

    def __init__(self, img_ruta,xy, camara,img_laberinto):
        self.camara = camara
        self.img_ori = pygame.image.load(img_ruta)
        self.img = self.img_ori
        self.x = xy[0]-32
        self.y = xy[1]-32
        self.unidad_de_avance=0.7
        self.x_cambio = 1.0
        self.y_cambio = 1.0
        self.muerto=False
        self.img_laberinto=img_laberinto

    def morir(self):
        self.muerto=True
        self.x=-100
        self.y=-100

    # Funcion que dibuja el enemigo
    def dibujar(self):
        self.mover()
        if not self.muerto:
            self.camara.dibujar(self.img, self.x, self.y)

    def mover(self):
        # restringimos los movimientos para que no se escape de la pantalla

        avance_normal = [self.x_cambio,self.y_cambio]

        avance_normal = comunes.avanzar_segun_laberinto((self.x, self.y), avance_normal, (64, 64), comunes.INTERACCION_REBOTAR)

        self.x_cambio=avance_normal[0]
        self.y_cambio=avance_normal[1]

        self.x += self.x_cambio
        self.y += self.y_cambio

