import pygame
import time 

bordeXp = 700
bordeXn = -10
bordeYp = 635
bordeYn = 360

class Player:
    #Sprites del jugador
    walking = [pygame.image.load("character/walking1.png"), pygame.image.load("character/walking2.png")]
    stand = pygame.image.load("character/bigsadboy.png") 
    suicide = [pygame.image.load('character/boypointing.png'), pygame.image.load('character/boypointing2.png'), pygame.image.load('character/shot1.png'), pygame.image.load('character/shot2.png', 'character/shot3.png')]
    dead = pygame.image.load("character/shot3.png") 
    ghost  = pygame.image.load("character/spirit.png")

    #Inventario del jugador (Cuantas encarnaciones y muertes tiene disponibles)
    num_encarnaciones = 3
    num_balas = 3

    #Tamaño del jugador en la pantalla
    scaleX = 120
    scaleY = 170
    
    #Ubicacion del jugador
    playerX = 600
    playerY = 600

    #Ubicacion del cadaver del jugador
    cadaverX = 1000
    cadaverY = 1000

    #Variable auxiliar para las animaciones
    pose = 1
    #Este es el estado en el que se encuentra el jugador para saber que animación o sprite hay que cargar
    #      "PARADO"        "CAMINANDO"               "SUICIDIO"       "MUERTO"       "FANTASMA"
    estado = "PARADO"
    #dirección en la que está mirando el jugador                         0 = Izquierda         1 = Derecha
    direccion = 0

    #funciones de la clase
    def pintarJugador(self, sprite, screen):
        if sprite == "PARADO":
            stand = pygame.transform.scale(self.stand, (self.scaleX, self.scaleY))
            if self.direccion == 1:
                stand = pygame.transform.flip(stand, True, False)
            screen.blit(stand, (self.playerX, self.playerY))

        elif sprite == "MUERTO":
            dead = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
            if self.direccion == 1:
                dead = pygame.transform.flip(dead, True, False)
            screen.blit(dead, (self.playerX, self.playerY))
            self.estado = "FANTASMA"
       
        elif sprite == "FANTASMA":
            ghost = pygame.transform.scale(self.ghost, (self.scaleX, self.scaleY))
            if self.direccion == 1:
                ghost = pygame.transform.flip(ghost, True, False)
            
            dead = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
            screen.blit(dead, (self.cadaverX, self.cadaverY))
            screen.blit(ghost, (self.playerX, self.playerY))
        
        elif sprite == "CAMINANDO":
                #Esta sección corresponde a la animación de caminar del personaje
                walking = pygame.transform.scale(self.walking[0], (self.scaleX, self.scaleY))
                self.pose += 1
                if  30 <= self.pose <= 60:
                     walking = pygame.transform.scale(self.walking[1], (self.scaleX, self.scaleY))
                     self.pose += 1
                if self.pose >= 60 :
                    self.pose = 0

                if self.direccion == 1:
                    walking = pygame.transform.flip(walking, True, False)
                screen.blit(walking, (self.playerX, self.playerY))
        
        elif sprite == "SUICIDIO":
                self.cadaverX = self.playerX
                self.cadaverY = self.playerY
                #Esta sección corresponde a la animación de suicidio de personaje
                if  1 <= self.pose <= 29:
                    suicide = pygame.transform.scale(self.suicide[0], (self.scaleX, self.scaleY))
                    if self.direccion == 1:
                            suicide = pygame.transform.flip(suicide, True, False)
                    screen.blit(suicide, (self.playerX, self.playerY))
                    self.pose += 1
                if  30 <= self.pose <= 50:
                            suicide = pygame.transform.scale(self.suicide[1], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if  51 <= self.pose <= 70:
                            suicide = pygame.transform.scale(self.suicide[2], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if  70 <= self.pose <= 105:
                            suicide = pygame.transform.scale(self.suicide[3], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if self.pose >= 105 :
                            suicide = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.estado = "MUERTO"
                            if self.pose >=120:
                                self.pose = 0

    def movimientos(self, event, screen):
          if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 0
                if self.playerX >= bordeXn:
                    self.playerX -=2

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 1
                if(self.playerX <= bordeXp):
                    self.playerX +=2

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                if self.playerY >= bordeYn:
                    self.playerY -=2
            
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                if self.playerY <= bordeYp:
                    self.playerY +=2
            
            if event.key == pygame.K_SPACE:
                if self.estado != "FANTASMA":
                    self.estado = "SUICIDIO"

          elif  event.type == pygame.KEYUP:
            if self.estado !="SUICIDIO" and self.estado!="FANTASMA":
                    self.estado = "PARADO"

    def HUD(self, screen):
        return 0
                

class Stage:
    #Imagenes utilizadas en los niveles
    fondos = pygame.image.load("backgrounds/fondo.png")
    pentagrama = pygame.image.load("items/penta.png")
    bala = pygame.image.load("items/bullet.png")
    pistola = pygame.image.load("items/gun.png")
    obstaculos = 0

    #Items de los niveles
    numPenta = 3
    numBalas = 3
    numObst = 3

    #Coordenadas de los items
    pentagramas = []
    balas =     []
    obstaculos = []

    #Dimensiones del nivel 
    stageX = 800
    stageY = 800

    #Meta del nivel 
    metaX = 800
    metaY = 800

    #funciones
    def pintarFondo(self, fondo, screen):
        fondo = pygame.image.load("backgrounds/fondo.png")
        screen.blit(fondo, (0, 0))

    def pintarItems(self):
        return 0

    def ganar(self, player):
        if player.playerX == self.metaX and player.playerY == self.metaY:
            return True
        return False



