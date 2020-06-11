import pygame
import comunes
import math
from Bala import Bala
from Camara import Camara
from pygame import mouse



class jugador:

    # Constructor def __init__(self, atributos)
    def __init__(self, img_ruta, x, y, screen,camara, img_bala_ruta, img_laberinto):
        self.camara=camara
        self.img_ori = pygame.image.load(img_ruta)
        self.img = self.img_ori
        self.x = x
        self.y = y
        self.x_cambio = 0.0
        self.y_cambio = 0.0
        self.unidad_de_avance = 5
        self.ang = 0.0
        self.screen = screen
        self.avanzar = False
        self.retroceder = False
        self.img_laberinto=img_laberinto
        self.ancho=64
        self.alto=64

        # Bala
        self.bala = Bala(img_bala_ruta, screen,self.camara)


    # Funcion que dibuja el player
    def dibujar(self, x, y,mouse_x,mouse_y):
        self.mover_jugador()
        self.rotar_jugador(mouse_x,mouse_y)
        self.camara.dibujar(self.img, x, y)

    def tecla_presionada(self, eventkey):
        if eventkey == pygame.K_w:
            self.avanzar = True
            self.retroceder = False
        if eventkey == pygame.K_s:
            self.retroceder = True
            self.avanzar = False
        if eventkey==pygame.K_SPACE:
            self.disparar()

    def disparar(self):
        if self.bala.quieta:
            self.bala.x = self.x
            self.bala.y = self.y
            self.bala.ang = self.ang
            self.bala.quieta=False
            self.bala.mover_bala()

    def tecla_levantada(self, eventkey):

        if eventkey == pygame.K_w:
            self.avanzar = False
            detener_avance = comunes.avanzar(self.x_cambio, self.y_cambio, -self.unidad_de_avance, self.ang )
            self.x_cambio = detener_avance[0]
            self.y_cambio = detener_avance[1]
        if eventkey == pygame.K_s:
            self.retroceder = False
            detener_retroceso = comunes.avanzar(self.x_cambio, self.y_cambio, -self.unidad_de_avance, self.ang + 180)
            self.x_cambio = detener_retroceso[0]
            self.y_cambio = detener_retroceso[1]

    def mover_jugador(self):

        # Movemos el jugador segun la tecla presionada
        avance_normal=[0.0,0.0]

        if self.avanzar:
            avance_normal = comunes.avanzar(self.x_cambio, self.y_cambio, self.unidad_de_avance, self.ang)
        if self.retroceder:
            avance_normal = comunes.avanzar(self.x_cambio, self.y_cambio, self.unidad_de_avance, self.ang + 180)

        self.x_cambio = avance_normal[0]
        self.y_cambio = avance_normal[1]

        #Se fija si el punto central de la nave al moverse va a entrar en una zona blanca
        try:
            tmp_x=int(self.x + self.x_cambio+ self.ancho/2)
            tmp_y=int(self.y + self.y_cambio+ self.ancho/2)
            if (self.img_laberinto.get_at((tmp_x , tmp_y ))[2]) == 255:
                self.y += self.y_cambio
                self.x += self.x_cambio
            # Deslizarse. Si no puede ir para adelante pero puede ir al costado o viceversa que lo haga
            elif (self.img_laberinto.get_at((tmp_x, int(self.y + self.ancho/2)))[2]) == 255:
                self.x += self.x_cambio
            elif (self.img_laberinto.get_at((int(self.x + self.ancho/2), tmp_y ))[2]) == 255:
                self.y += self.y_cambio
        except:
            pass

        # la camara sigue al jugador
        if (self.x - self.camara.x)<200:
            self.camara.set_x( self.camara.x - abs(self.x_cambio))
        elif (self.x - self.camara.x)>400:
            self.camara.set_x( self.camara.x + abs(self.x_cambio))
        if (self.y - self.camara.y)<200:
            self.camara.set_y( self.camara.y - abs(self.y_cambio))
        elif (self.y - self.camara.y)>400:
            self.camara.set_y( self.camara.y + abs(self.y_cambio))

        #mover bala
        self.bala.mover_bala()

    def rotar_jugador(self,mouse_x,mouse_y):
        self.ang = math.atan2(-(mouse_y - (600/2)), (mouse_x - (800/2) + 0.0000001))

        if mouse.get_pos()[0]>((800/2)+100):
            mx=(800/2)+100
            mouse.set_pos(mx,mouse.get_pos()[1])
        elif mouse.get_pos()[0]<((800/2)-100):
            mx=(800 / 2) - 100
            mouse.set_pos(mx,mouse.get_pos()[1])
        if mouse.get_pos()[1]>((600/2)+100):
            my=(600 / 2) + 100
            mouse.set_pos(mouse.get_pos()[0],my)
        elif mouse.get_pos()[1] < ((600 / 2) - 100):
            my = (600 / 2) - 100
            mouse.set_pos(mouse.get_pos()[0],my)




        self.ang = self.ang * (180 / math.pi)
        self.img = comunes.rot_center(self.img_ori, self.ang + 90 + 180)
