import pygame
import time 
import random
import music
import window
from pygame import gfxdraw

class Player:

    def __init__(self):
        #Ubicaciones del cadaver del jugador en caso de que sea un fantasma
        self.cadaverX = 1000
        self.cadaverY = 1000

        #Dimensiones del sprite del jugador
        self.scaleX = 80
        self.scaleY = 130

        #Numero de balas que tiene el jugador
        self.num_balas = 3

        #Ubicación del jugador
        self.playerX = 500
        self.playerY = 300

        #Variable auxiliar para calcular el tiempo que debe de durar cada sprite en una animación
        self.pose = 1
        #Posibles estados en los que puede estar el jugador
        #PARADO         CAMINANDO       SUICIDIO        FANTASMA      MUERTO    DISPARANDO
        self.estado = "PARADO"
        #Dirección en la que está mirando el jugador
        # 0 = IZQUIERDA         1 = DERECHA         2 = ARRIBA          3 =ABAJO
        self.direccion = 0
        #Velocidad  de movimiento del jugador
        self.velocidad = 4

        #Dirección y coordenadas iniciales de una bala disparada
        self.balaX = self.playerX + 25
        self.balaY = self.playerY + 55
        self.direccionBala = self.direccion

        #Sprites del jugador
        self.walking = [pygame.image.load("character/walking1.png"), pygame.image.load("character/walking2.png")]
        self.walkingFront = [pygame.image.load("character/front1.png"), pygame.image.load("character/front2.png")]
        self.walkingBack = [pygame.image.load("character/back1.png"), pygame.image.load("character/back2.png")]
        self.stand = pygame.image.load("character/bigsadboy.png") 
        self.standFront = pygame.image.load("character/front.png")
        self.standBack = pygame.image.load("character/back.png")
        self.shooting = pygame.image.load("character/shooting.png")
        self.shootFront = pygame.image.load("character/frontshoot.png")
        self.shootBack = pygame.image.load("character/backshoot.png")
        self.suicide = [pygame.image.load('character/boypointing.png'), pygame.image.load('character/boypointing2.png'), pygame.image.load('character/shot1.png'), pygame.image.load('character/shot2.png', 'character/shot3.png')]
        self.dead = pygame.image.load("character/shot3.png") 
        self.ghost  = pygame.image.load("character/spirit.png")

        self.disparo = pygame.image.load("items/bullet.png")
        self.disparo = pygame.transform.scale(self.disparo, (8,8))
        self.disparo = pygame.transform.rotate(self.disparo, 90)
        
        #Variable auxiliar para saber si el jugador ha disparado 
        self.shoot = False


        """
            Esta funcion muestra al jugador en pantalla (Y sus balas)
            sprite =          Estado en el que se encuentra el jugadir
            screen =        Ventana en la que está corriendo el juego
            stage =          El nivel que está corriendo en el juego
        """
    def pintarJugador(self, sprite, screen, stage):
        #Si el jugador no se está moviendo lo trazamos parado
        if sprite == "PARADO":
            if self.direccion == 0: 
                stand = pygame.transform.scale(self.stand, (self.scaleX, self.scaleY))
            elif self.direccion == 1:
                stand = pygame.transform.flip(pygame.transform.scale(self.stand, (self.scaleX, self.scaleY)), True, False)
            elif self.direccion == 2:
                stand = pygame.transform.scale(self.standBack, (self.scaleX, self.scaleY))
            else:
                stand = pygame.transform.scale(self.standFront, (self.scaleX, self.scaleY))

            screen.blit(stand, (self.playerX, self.playerY))

        #Si el jugador se encuentra muerto trazamos su cadaver
        elif sprite == "MUERTO":
            dead = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
            if self.direccion == 1:
                dead = pygame.transform.flip(dead, True, False)
            screen.blit(dead, (self.playerX, self.playerY))
            self.estado = "FANTASMA"

       #Si el jugador se encuentra muerto lo dibujamos en su forma fantasma
        elif sprite == "FANTASMA":
            dead = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
            screen.blit(dead, (self.cadaverX, self.cadaverY))

            if self.playerX in  range (stage.pentaX-30, stage.pentaX+45) and self.playerY in range(stage.pentaY-64, stage.pentaY+40):
                    screen.blit(stage.fuego, (stage.pentaX+25, stage.pentaY-20))
            else:
                ghost = pygame.transform.scale(self.ghost, (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    ghost = pygame.transform.flip(ghost, True, False)
                screen.blit(ghost, (self.playerX, self.playerY))
        
        #Si el usuario esta en movimiento trazamos la animación de caminar
        elif sprite == "CAMINANDO":
                if self.direccion == 0 or self.direccion == 1:
                    animacion = self.walking;
                elif self.direccion == 2:
                    animacion = self.walkingBack
                elif self.direccion == 3:
                    animacion = self.walkingFront

                walking = pygame.transform.scale(animacion[0], (self.scaleX, self.scaleY))
                self.pose += 1
                if  10 <= self.pose <= 25:
                     walking = pygame.transform.scale(animacion[1], (self.scaleX, self.scaleY))
                     self.pose += 1
                if self.pose >= 25 :
                    self.pose = 0

                if self.direccion == 1:
                    walking = pygame.transform.flip(walking, True, False)
                screen.blit(walking, (self.playerX, self.playerY))
        
        #Si el jugador ha decidido disparar cargamos la animacion de disparo
        elif sprite == "DISPARANDO":
                if self.direccion == 0:
                    shooting = pygame.transform.scale(self.shooting, (self.scaleX, self.scaleY))
                elif self.direccion == 1:
                    shooting = pygame.transform.flip(pygame.transform.scale(self.shooting, (self.scaleX, self.scaleY)), True, False)
                elif self.direccion == 2:
                    shooting = pygame.transform.scale(self.shootBack, (self.scaleX, self.scaleY))
                else:
                    shooting = pygame.transform.scale(self.shootFront, (self.scaleX, self.scaleY))
                screen.blit(shooting, (self.playerX, self.playerY))

        #Si el jugador ha decidido quitarse la vida cargamos la animacion de suicidio
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
                if  30 <= self.pose <= 35:
                            suicide = pygame.transform.scale(self.suicide[1], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if  35 <= self.pose <= 42:
                            suicide = pygame.transform.scale(self.suicide[2], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if  42 <= self.pose <= 70:
                            suicide = pygame.transform.scale(self.suicide[3], (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))
                            self.pose += 1
                if self.pose >= 70 :
                            suicide = pygame.transform.scale(self.dead, (self.scaleX, self.scaleY))
                            if self.direccion == 1:
                                suicide = pygame.transform.flip(suicide, True, False)
                            screen.blit(suicide, (self.playerX, self.playerY))

                            self.num_balas -=1
                            self.estado = "MUERTO"
                            if self.pose >=120:
                                self.pose = 0

        #En caso de que el usuario haya disparado trazamos la trayectoria del disparo
        if self.shoot:    
                if self.direccionBala == 0:
                    self.balaX -= 20
                    screen.blit(self.disparo, (self.balaX, self.balaY))  
                elif self.direccionBala == 1:
                    self.balaX += 20
                    screen.blit(self.disparo, (self.balaX, self.balaY))  
                elif self.direccionBala == 2:
                    self.balaY -= 20
                    screen.blit(self.disparo, (self.balaX, self.balaY))  
                else:
                    self.balaY += 20
                    screen.blit(self.disparo, (self.balaX, self.balaY)) 

                if (self.balaX >= window.windowX or  self.balaX <= 0 or self.balaY >= window.windowY or  self.balaY <= 0):
                    self.shoot = False
                    self.num_balas -= 1
                    self.balaX = self.playerX + 25
                    self.balaY = self.playerY + 55

        """
            Esta funcion regula las animaciones y acciones del jugador en base a las entradas de teclado y mouse introducidad
            event =          Entrada recibida
            screen =        Ventana en la que está corriendo el juego
            stage =          El nivel que está corriendo en el juego
        """
    def movimientos(self, event, stage):
        #En caso de que el jugador sea un fantasma y se haya parado en el centro de un pentagrama, revivimos su cadaver
          if self.playerX in  range (stage.pentaX-30, stage.pentaX+45) and self.playerY in range(stage.pentaY-64, stage.pentaY+40) and self.estado == "FANTASMA":
                self.pose = 0
                while self.pose <=10000000:
                    self.pose+=1
                if self.pose >= 10000000:
                    self.estado = "PARADO"
                    self.playerX = self.cadaverX
                    self.playerY = self.cadaverY
                self.pose = 0
        
         #Este condicional es accedido siempre que se haya pulsado una tecla
          if event.type == pygame.KEYDOWN:
            #Desplazamiento a la izquierda
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 0
                if self.playerX >= 0:
                    self.playerX -=self.velocidad

            #Desplazamiento a la derecha
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 1
                if(self.playerX <=window.windowX-80):
                    self.playerX +=self.velocidad

            #Desplazamiento hacia arriba
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 2
                if self.playerY >= 0:
                    self.playerY -=self.velocidad
            
            #Desplazamiento hacia abajo
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 3
                if self.playerY <= window.windowY-130:
                    self.playerY +=self.velocidad
            
            #Suicidio del jugador
            if event.key == pygame.K_SPACE:
                if self.estado != "FANTASMA" and self.num_balas > 0:
                    self.estado = "SUICIDIO"
            
            #Jugador dispara
            if event.key == pygame.K_q:
                if (self.estado == "CAMINANDO" or self.estado == "PARADO") and self.num_balas > 0:   
                    self.estado = "DISPARANDO"
                    self.balaX = self.playerX + 25
                    self.balaY = self.playerY + 55
                    self.direccionBala = self.direccion
                    self.shoot = True
          
          #Si no se está pulsando ninguna tecla, el jugador se encontrará parado
          elif  event.type == pygame.KEYUP:
            if self.estado !="SUICIDIO" and self.estado!="FANTASMA":
                    self.estado = "PARADO"

    """
            Esta funcion muestra el HUD con los datos del jugador en la pantalla
            screen =        Ventana en la que está corriendo el juego
    """
    def HUD(self, screen, stage):
        myfont = pygame.font.SysFont("Comic Sans MS", 30)

        label1 = myfont.render("Bullets:", 1, (255,255,255))
        screen.blit(label1, (40, 690))

        screen.blit(pygame.transform.rotate(stage.bala, -20), (40, 715))
        label2 = myfont.render(("X " + str(self.num_balas)), 1, (0,0,0))
        screen.blit(label2, (85, 730))


class Stage:

    def __init__(self):
        #Coordenadas del pentagrama en el nivel
        self.pentaX = 32
        self.pentaY = 300

        #Imagenes que utilizamos para armar el nivel 
        self.fondos = pygame.image.load("backgrounds/fondo.png")
        self.pentagrama = pygame.image.load("items/penta.png")
        self.pentagrama = pygame.transform.scale(self.pentagrama, (150, 100))
        self.bala = pygame.image.load("items/bullet.png")
        self.bala = pygame.transform.scale(self.bala, (20, 40))
        self.pistola = pygame.image.load("items/gun.png")
        self.fuego = pygame.image.load("items/fuego.png")
        self.fuego = pygame.transform.scale(self.fuego, (100, 100))

    def pintarFondo(self, fondo, screen):
        fondo = pygame.image.load("backgrounds/fondo.png")
        fondo = pygame.transform.scale(fondo, (window.windowX, window.windowY))
        screen.blit(fondo, (0, 0))
        self.pintarItems(screen)

    def pintarItems(self, screen):
        screen.blit(self.pentagrama, (self.pentaX, self.pentaY))




