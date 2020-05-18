import pygame
import time
import random
import window
import copy
from pygame import gfxdraw

#Esta sección del código maneja todos los sonidos del juego
#Guardamos todos los sonidos que usaremos
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
music = pygame.mixer.music.load("./sounds/levelSong.wav")
ammoGrab = pygame.mixer.Sound("./sounds/ammo.wav")
defeat = pygame.mixer.Sound("./sounds/defeat.wav")
noAmmo = pygame.mixer.Sound("./sounds/emptyGun.wav")
shot = pygame.mixer.Sound("./sounds/gunshot.wav")
hurt = pygame.mixer.Sound("./sounds/hurt.wav")
pentagram = pygame.mixer.Sound("./sounds/pentagram.wav")
enemySpawn = pygame.mixer.Sound("./sounds/spawn.wav")
win = pygame.mixer.Sound("./sounds/victory.wav")
zombieDeath = pygame.mixer.Sound("./sounds/zombieSounds/zombieDeath.wav")

zombieAgro = [pygame.mixer.Sound("./sounds/zombieSounds/zSound1.wav"), 
pygame.mixer.Sound("./sounds/zombieSounds/zSound2.wav"), 
pygame.mixer.Sound("./sounds/zombieSounds/zSound3.wav"), 
pygame.mixer.Sound("./sounds/zombieSounds/zSound4.wav")]
#Reproducimos la musica del nivel en loop
pygame.mixer.music.play(-1)
#Hacemos ajustes de volumen
channel=pygame.mixer.find_channel(True)
channel.set_volume(1.0)



class Player:

    def __init__(self):
        
        # Ubicaciones del cadaver del jugador en caso de que sea un fantasma
        self.cadaverX = 1000
        self.cadaverY = 1000

        # Dimensiones del sprite del jugador
        self.scaleX = 60
        self.scaleY = 110

        # Numero de balas que tiene el jugador
        self.num_balas = 3

        # Ubicación del jugador
        self.playerX = 500
        self.playerY = 300

        # Variable auxiliar para calcular el tiempo que debe de durar cada sprite en una animación
        self.pose = 1
        # Posibles estados en los que puede estar el jugador
        # PARADO         CAMINANDO       SUICIDIO        FANTASMA      MUERTO    DISPARANDO
        self.estado = "PARADO"
        # Dirección en la que está mirando el jugador
        # 0 = IZQUIERDA         1 = DERECHA         2 = ARRIBA          3 =ABAJO
        self.direccion = 0
        # Velocidad  de movimiento del jugador
        self.velocidad = 4
        self.velocidadFantasma = 11

        # Dirección y coordenadas iniciales de una bala disparada
        self.balaX = self.playerX + 25
        self.balaY = self.playerY + 55
        self.direccionBala = self.direccion

        # Numero de enemigos que el jugador necesita eliminar para ganar
        self.winGoal = 1
        # Numero de enemigos eliminados del jugador
        self.killed = 0

        #Esta variable la usamos para controlar la reproducción
        #de algunos sonidos
        self.reproduce = True

        # Salud del jugador
        self.health = 3

        # Sprites del jugador
        self.walking = [pygame.image.load(
            "character/walking1.png"), pygame.image.load("character/walking2.png")]
        self.walkingFront = [pygame.image.load(
            "character/front1.png"), pygame.image.load("character/front2.png")]
        self.walkingBack = [pygame.image.load(
            "character/back1.png"), pygame.image.load("character/back2.png")]
        self.stand = pygame.image.load("character/bigsadboy.png")
        self.standFront = pygame.image.load("character/front.png")
        self.standBack = pygame.image.load("character/back.png")
        self.shooting = pygame.image.load("character/shooting.png")
        self.shootFront = pygame.image.load("character/frontshoot.png")
        self.shootBack = pygame.image.load("character/backshoot.png")
        self.suicide = [pygame.image.load('character/boypointing.png'), pygame.image.load('character/boypointing2.png'),
                        pygame.image.load('character/shot1.png'), pygame.image.load('character/shot2.png', 'character/shot3.png')]
        self.dead = pygame.image.load("character/shot3.png")
        self.ghost = pygame.image.load("character/spirit.png")

        self.disparo = pygame.image.load("items/bullet.png")
        self.disparo = pygame.transform.scale(self.disparo, (8, 8))
        self.disparo = pygame.transform.rotate(self.disparo, 90)

        # Variable auxiliar para saber si el jugador ha disparado
        self.shoot = False

        """
            Esta funcion muestra al jugador en pantalla (Y sus balas)
            sprite =          Estado en el que se encuentra el jugadir
            screen =        Ventana en la que está corriendo el juego
            stage =          El nivel que está corriendo en el juego
        """

    def pintarJugador(self, sprite, screen, stage):
        # Si el jugador no se está moviendo lo trazamos parado
        if sprite == "PARADO":
            if self.direccion == 0:
                stand = pygame.transform.scale(
                    self.stand, (self.scaleX, self.scaleY))
            elif self.direccion == 1:
                stand = pygame.transform.flip(pygame.transform.scale(
                    self.stand, (self.scaleX, self.scaleY)), True, False)
            elif self.direccion == 2:
                stand = pygame.transform.scale(
                    self.standBack, (self.scaleX, self.scaleY))
            else:
                stand = pygame.transform.scale(
                    self.standFront, (self.scaleX, self.scaleY))

            screen.blit(stand, (self.playerX, self.playerY))

        # Si el jugador se encuentra muerto trazamos su cadaver
        elif sprite == "MUERTO":
            dead = pygame.transform.scale(
                self.dead, (self.scaleX, self.scaleY))
            if self.direccion == 1:
                dead = pygame.transform.flip(dead, True, False)
            screen.blit(dead, (self.playerX, self.playerY))
            if self.health == 0:
                self.direccion = 0
                return
            # El jugador solo se hará fantasma si tiene vida
            self.estado = "FANTASMA"

       # Si el jugador se encuentra muerto lo dibujamos en su forma fantasma
        elif sprite == "FANTASMA":
            dead = pygame.transform.scale(
                self.dead, (self.scaleX, self.scaleY))
            screen.blit(dead, (self.cadaverX, self.cadaverY))

            if self.playerX in range(stage.pentaX-30, stage.pentaX+60) and self.playerY in range(stage.pentaY-64, stage.pentaY+40):
                screen.blit(stage.fuego, (stage.pentaX+25, stage.pentaY-20))
            else:
                ghost = pygame.transform.scale(
                    self.ghost, (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    ghost = pygame.transform.flip(ghost, True, False)
                screen.blit(ghost, (self.playerX, self.playerY))

        # Si el usuario esta en movimiento trazamos la animación de caminar
        elif sprite == "CAMINANDO":
            if self.direccion == 0 or self.direccion == 1:
                animacion = self.walking
            elif self.direccion == 2:
                animacion = self.walkingBack
            elif self.direccion == 3:
                animacion = self.walkingFront

            walking = pygame.transform.scale(
                animacion[0], (self.scaleX, self.scaleY))
            self.pose += 1
            if 10 <= self.pose <= 25:
                walking = pygame.transform.scale(
                    animacion[1], (self.scaleX, self.scaleY))
                self.pose += 1
            if self.pose >= 25:
                self.pose = 0

            if self.direccion == 1:
                walking = pygame.transform.flip(walking, True, False)
            screen.blit(walking, (self.playerX, self.playerY))

        # Si el jugador ha decidido disparar cargamos la animacion de disparo
        elif sprite == "DISPARANDO":
            if self.direccion == 0:
                shooting = pygame.transform.scale(
                    self.shooting, (30 + self.scaleX, self.scaleY))
            elif self.direccion == 1:
                shooting = pygame.transform.flip(pygame.transform.scale(
                    self.shooting, (self.scaleX + 20, self.scaleY)), True, False)
            elif self.direccion == 2:
                shooting = pygame.transform.scale(
                    self.shootBack, (self.scaleX, self.scaleY))
            else:
                shooting = pygame.transform.scale(
                    self.shootFront, (self.scaleX, self.scaleY))
            screen.blit(shooting, (self.playerX, self.playerY))

        # Si el jugador ha decidido quitarse la vida cargamos la animacion de suicidio
        elif sprite == "SUICIDIO":
            self.cadaverX = self.playerX
            self.cadaverY = self.playerY
            # Esta sección corresponde a la animación de suicidio de personaje
            if 1 <= self.pose <= 29:
                suicide = pygame.transform.scale(
                    self.suicide[0], (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    suicide = pygame.transform.flip(suicide, True, False)
                screen.blit(suicide, (self.playerX, self.playerY))
                self.pose += 1
            if 30 <= self.pose <= 35:
                suicide = pygame.transform.scale(
                    self.suicide[1], (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    suicide = pygame.transform.flip(suicide, True, False)
                screen.blit(suicide, (self.playerX, self.playerY))
                self.pose += 1
            if 35 <= self.pose <= 42:
                suicide = pygame.transform.scale(
                    self.suicide[2], (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    suicide = pygame.transform.flip(suicide, True, False)
                screen.blit(suicide, (self.playerX, self.playerY))
                #Sonido de disparo
                if self.reproduce:
                    channel.play(shot)
                    self.reproduce = False
                self.pose += 1
            if 42 <= self.pose <= 70:
                suicide = pygame.transform.scale(
                    self.suicide[3], (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    suicide = pygame.transform.flip(suicide, True, False)
                screen.blit(suicide, (self.playerX, self.playerY))
                self.pose += 1
            if self.pose >= 70:
                suicide = pygame.transform.scale(
                    self.dead, (self.scaleX, self.scaleY))
                if self.direccion == 1:
                    suicide = pygame.transform.flip(suicide, True, False)
                screen.blit(suicide, (self.playerX, self.playerY))
                self.num_balas -= 1
                self.estado = "MUERTO"
                self.reproduce = True
                if self.pose >= 70:
                    self.pose = 0

        # En caso de que el usuario haya disparado trazamos la trayectoria del disparo
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

            if (self.balaX >= window.windowX or self.balaX <= 0 or self.balaY >= window.windowY or self.balaY <= 0):
                self.shoot = False
                self.balaX = self.playerX + 25
                self.balaY = self.playerY + 55

        """
            Esta funcion regula las animaciones y acciones del jugador en base a las entradas de teclado y mouse introducidad
            event =          Entrada recibida
            screen =        Ventana en la que está corriendo el juego
            stage =          El nivel que está corriendo en el juego
        """

    def movimientos(self, event, stage):

        # Si el jugador está muerto evidentemente no se podrá mover, si ha ganado el juego ha terminado entonces tampoco
        if self.health == 0 or self.killed >= self.winGoal:
            return

        # En caso de que el jugador sea un fantasma y se haya parado en el centro de un pentagrama, revivimos su cadaver
        if self.playerX in range(stage.pentaX-30, stage.pentaX+60) and self.playerY in range(stage.pentaY-64, stage.pentaY+40) and self.estado == "FANTASMA":
            #Reproducimos sonido del pentagrama
            if self.reproduce:
                channel.play(pentagram)
                self.reproduce = False
            self.pose = 0
            while self.pose <= 10000000:
                self.pose += 1
            if self.pose >= 10000000:
                self.estado = "PARADO"
                self.playerX = self.cadaverX
                self.playerY = self.cadaverY
                self.reproduce = True
            self.pose = 0

            # En caso de que el jugador esté vivo y se haya parado sobre una recarga de munición aumentamos sus balas
        if self.playerX in range(stage.ubicacion[0]-50, stage.ubicacion[0]+45) and self.playerY in range(stage.ubicacion[1]-120, stage.ubicacion[1]+40):
            self.num_balas += 5
            #Reproducimos sonido
            channel.play(ammoGrab)
            if stage.ubicacion == stage.ubicaciones_balas[0]:
                stage.ubicacion = stage.ubicaciones_balas[1]
            else:
                stage.ubicacion = stage.ubicaciones_balas[0]

        # Si el jugador se queda sin balas y la recarga está en un lugar inaccesible para el, la cambiamos de lugar para que pueda
        # seguir jugando y que no quede condenado a perder
        if self.num_balas == 0 and stage.ubicacion == stage.ubicaciones_balas[1] and self.estado != "SUICIDIO" and self.estado != "FANTASMA":
            stage.ubicacion = stage.ubicaciones_balas[2]

            # Este condicional es accedido siempre que se haya pulsado una tecla
            # Si el jugador se está suicidando no interrumpimos esa animación
            # ignoramos cualquier tecla pulsada hasta que termine el suicidio
        if event.type == pygame.KEYDOWN and self.estado != "SUICIDIO" and self.estado != "MUERTO":

            # Desplazamiento a la izquierda
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 0
                if self.playerX >= 0:
                    # 3
                    if self.estado == "FANTASMA":
                        self.playerX -= self.velocidadFantasma

                    elif ((self.playerY in stage.fronterasLavaY and self.playerX-5 not in stage.fronterasLavaX) or self.playerY not in stage.fronterasLavaY):
                        if ((self.playerY in stage.fronterasHoyoY and self.playerX-5 not in stage.fronterasHoyoX) or self.playerY not in stage.fronterasHoyoY):
                            self.playerX -= self.velocidad

            # Desplazamiento a la derecha
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 1
                if(self.playerX <= window.windowX-80):
                    # 3
                    if self.estado == "FANTASMA":
                        self.playerX += self.velocidadFantasma

                    elif ((self.playerY in stage.fronterasLavaY and self.playerX+5 not in stage.fronterasLavaX) or self.playerY not in stage.fronterasLavaY):
                        if ((self.playerY in stage.fronterasHoyoY and self.playerX+5 not in stage.fronterasHoyoX) or self.playerY not in stage.fronterasHoyoY):
                            self.playerX += self.velocidad

            # Desplazamiento hacia arriba
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 2
                if self.playerY >= 0:
                    # 3
                    if self.estado == "FANTASMA":
                        self.playerY -= self.velocidadFantasma

                    elif ((self.playerX in stage.fronterasLavaX and self.playerY-5 not in stage.fronterasLavaY) or self.playerX not in stage.fronterasLavaX):
                        if ((self.playerX in stage.fronterasHoyoX and self.playerY-5 not in stage.fronterasHoyoY) or self.playerX not in stage.fronterasHoyoX):
                            self.playerY -= self.velocidad

            # Desplazamiento hacia abajo
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.estado != "FANTASMA":
                    self.estado = "CAMINANDO"
                self.direccion = 3
                if self.playerY <= window.windowY-130:
                    # 3
                    if self.estado == "FANTASMA":
                        self.playerY += self.velocidadFantasma

                    elif (self.playerX in stage.fronterasLavaX and self.playerY+5 not in stage.fronterasLavaY) or self.playerX not in stage.fronterasLavaX:
                        if ((self.playerX in stage.fronterasHoyoX and self.playerY+5 not in stage.fronterasHoyoY) or self.playerX not in stage.fronterasHoyoX):
                            self.playerY += self.velocidad

            # Suicidio del jugador
            if event.key == pygame.K_SPACE:
                if self.estado != "FANTASMA" and self.num_balas > 0:
                    self.estado = "SUICIDIO"

            # Jugador dispara
            if event.key == pygame.K_q:
                #Sonido de disparo
                if self.reproduce and self.num_balas > 0:
                    channel.play(shot)
                    self.reproduce = False
                #Si no hay balas y el jugador disparó reproducimos sonido de 
                #pistola vacia
                if self.reproduce and self.num_balas <= 0:
                    channel.play(noAmmo)
                    self.reproduce = False

                if (self.estado == "CAMINANDO" or self.estado == "PARADO") and self.num_balas > 0:
                    self.num_balas -= 1
                    self.estado = "DISPARANDO"
                    self.balaX = self.playerX + 25
                    self.balaY = self.playerY + 55
                    self.direccionBala = self.direccion
                    self.shoot = True

        # Si no se está pulsando ninguna tecla, el jugador se encontrará parado
        elif event.type == pygame.KEYUP:
            self.reproduce = True
            if self.estado != "SUICIDIO" and self.estado != "FANTASMA":
                self.estado = "PARADO"

    """
            Esta funcion muestra el HUD con los datos del jugador en la pantalla
            screen =        Ventana en la que está corriendo el juego
    """

    def HUD(self, screen, stage, enemy):

        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        # Imprimimos la  cantidad de balas en pantalla para el jugador
        label1 = myfont.render("Bullets:", 1, (255, 255, 255))
        screen.blit(label1, (40, 690))
        screen.blit(pygame.transform.rotate(stage.bala, -20), (40, 715))
        label2 = myfont.render(("X " + str(self.num_balas)), 1, (0, 0, 0))
        screen.blit(label2, (85, 730))

        # Imprimimos la cantidad de zombies asesinados y faltantes
        # para el jugaor
        label3 = myfont.render("Zemons killed:", 1, (200, 100, 100))
        screen.blit(label3, (530, 690))
        label4 = myfont.render(
            (str(self.killed) + " / " + str(self.winGoal)), 1, (255, 255, 255))
        screen.blit(label4, (530, 725))

        # Imprimimos la salud del jugador
        label5 = myfont.render("Health:", 1, (255, 255, 255))
        screen.blit(label5, (270, 690))
        pos = 270
        for i in range(self.health):
            pygame.draw.rect(screen, (0, 255, 0), (pos, 735, 30, 30))
            pos += 40

        # Si el jugador ha perdido toda su vida, perdemos el juego
        # y le comunicamos las tristes noticias al jugador
        if self.health == 0:
            #Jazz music stops
            pygame.mixer.music.pause()
            #Reproducimos musica de derrota
            if self.reproduce:
                channel.play(defeat)
                self.reproduce = False
            myfont = pygame.font.SysFont("Comic Sans MS", 80)
            label6 = myfont.render("Has Perdido!", 1, (150, 30, 30))
            screen.blit(label6, (150, 300))
            # EL JUEGO HA TERMINADO

        # Si el jugador ha matado a los suficientes zombies anunciamos que el
        # juego se ha ganado
        if self.health > 0 and self.killed >= self.winGoal:
            #Jazz music stops
            pygame.mixer.music.pause()
            #Reproducimos musica de victoria
            if self.reproduce:
                channel.play(win)
                self.reproduce = False
            myfont = pygame.font.SysFont("Comic Sans MS", 80)
            label7 = myfont.render("Has Ganado!", 1, (30, 150, 30))
            screen.blit(label7, (150, 300))
            for key, value in enemy.enemies.items():
                value["estado"] = 0
            # EL JUEGO HA TERMINADO


class Stage:

    def __init__(self):
        # Coordenadas del pentagrama en el nivel
        self.pentaX = 60
        self.pentaY = 300

        # Coordenadas de las recargas de municion que hay en el nivel
        self.ubicaciones_balas = [(600, 300), (710, 100), (150, 550)]
        self.ubicacion = self.ubicaciones_balas[0]

        # Fronteras del nivel (Zonas no accesibles)
        self.fronterasLavaX = []
        self.fronterasLavaY = []
        self.fronterasHoyoX = []
        self.fronterasHoyoY = []
        # Definimos fronteras de la lava
        for x in range(600, 800):
            self.fronterasLavaX.append(x)
        for y in range(-100, 140):
            self.fronterasLavaY.append(y)
        # Definimos las fronteras de los cañones:
        for x in range(-20, 250):
            self.fronterasHoyoX.append(x)
        for y in range(340, 420):
            self.fronterasHoyoY.append(y)
        for y in range(120, 220):
            self.fronterasHoyoY.append(y)

        # Imagenes que utilizamos para armar el nivel
        self.fondos = pygame.image.load("backgrounds/fondo.png")
        self.pentagrama = pygame.transform.scale(
            pygame.image.load("items/penta.png"), (150, 100))
        self.bala = pygame.transform.scale(
            pygame.image.load("items/bullet.png"), (20, 40))
        self.bala = pygame.transform.rotate(self.bala, -45)
        self.fuego = pygame.transform.scale(
            pygame.image.load("items/fuego.png"), (100, 100))
        self.canon = pygame.transform.scale(
            pygame.image.load("backgrounds/canon.png"), (130, 65))
        self.hoyo = pygame.transform.scale(
            pygame.image.load("backgrounds/hoyo.png"), (55, 55))
        self.lava = pygame.transform.scale(
            pygame.image.load("backgrounds/lava.png"), (130, 50))
        self.pedestal = pygame.transform.scale(
            pygame.image.load("backgrounds/pedestal.png"), (240, 170))

    """
            Esta funcion pinta el fondo del nivel
            fondo =         imagen que se usará de fondo
            screen =        Ventana en la que está corriendo el juego
    """
    def pintarFondo(self, fondo, screen):
        fondo = pygame.image.load("backgrounds/fondo.png")
        fondo = pygame.transform.scale(fondo, (window.windowX, window.windowY))
        screen.blit(fondo, (0, 0))
        self.pintarObstaculos(screen)
        self.pintarItems(screen)

    """
            Esta funcion pinta los items del nivel
            screen =        Ventana en la que está corriendo el juego
    """

    def pintarItems(self, screen):
        screen.blit(self.pedestal, (self.pentaX-45, self.pentaY-25))
        screen.blit(self.pentagrama, (self.pentaX, self.pentaY))
        screen.blit(self.bala, (self.ubicacion))

    """
        Esta funcion pinta los obstaculos del nivel
        screen =        Ventana en la que está corriendo el juego
    """

    def pintarObstaculos(self, screen):
        # Lava del nivel
        screen.blit(self.lava, (640, 30))
        screen.blit(pygame.transform.rotate(self.lava, 90), (635, 80))
        screen.blit(pygame.transform.rotate(self.lava, 180), (640, 160))

        # Cañones del nivel
        screen.blit(self.canon, (30, 440))
        screen.blit(self.canon, (130, 440))
        screen.blit(self.canon, (30, 220))
        screen.blit(self.canon, (130, 220))


class Enemy:
    def __init__(self):

        # Sprites del enemigo
        self.walking = [pygame.image.load(
            "enemy/enemigo_walk1.png"), pygame.image.load("enemy/enemigo_walk2.png")]
        self.walkingFront = [pygame.image.load(
            "enemy/enemy_frontWalk1.png"), pygame.image.load("enemy/enemy_frontWalk2.png")]
        self.walkingBack = [pygame.image.load(
            "enemy/enemy_walkBack1.png"), pygame.image.load("enemy/enemy_walkBack2.png")]
        self.stand = pygame.image.load("enemy/enemigo_stand.png")
        self.standFront = pygame.image.load("enemy/enemy_standFront.png")
        self.standBack = pygame.image.load("enemy/enemy_standBack.png")
        self.fuego = pygame.transform.scale(
            pygame.image.load("items/fuego.png"), (70, 100))
        self.deadSide = pygame.image.load("enemy/enemy_death.png")
        self.deadFront = pygame.image.load("enemy/enemy_deathFront.png")
        self.deadBack = pygame.image.load("enemy/enemy_deathBack.png")

        # Dimensiones de los sprites
        self.scaleX = 60
        self.scaleY = 110

        # Cantidad de enemigos en el maps
        self.numEnemigos = 0

        # Cantidad máxima de enemigos en un nivel
        self.maxEnemigos = 100

        # Contador auxiliar para las transiciones de sprites
        self.spriteTimer = 0
        # Contador para frames de invensibilidad
        self.inv = 20

        # Velocidad de los enemigos
        self.velocidad = 1

        #Estas variable las usamos para controlar la reproducción
        #de algunos sonidos
        self.reproduce = True
        self.soundCounter = 0

        # Información sobre cada uno de los enemigos en el stage
        self.enemies = {}

        # Estructura del diccionario que contiene la información de los enemigos
        self.enemies[0] = {
            # Coordenadas de la ubicación del enemigo
            'coord': "",
            # Dirección en la que está observando el enemigo
            # 0 = IZQUIERDA         1 = DERECHA         2 = ARRIBA          3 =ABAJO
            'direccion': "",
            # Valor del contador auxiliar usado en la
            # transición de sprites
            'counter': "",
            # Posibles estados en los que puede estar el enemigo
            #   0 = MUERTO      1 = VIVO
            'estado': "",
            # Contador para llevar control del tiempo que un enemigo lleva muerto
            'deathCounter': ""
        }

    # Función que agrega (o no) un enemigo al nivel
    def spawn(self, stage, player):
        # Si el jugador ha muerto no spawneamos mas enemigos, o si ya ha ganado el juego
        if player.health == 0 or (player.killed >= player.winGoal):
            return

        # Si alcanzamos el máximo numero de enemigos, no spawneamos más
        if self.numEnemigos >= self.maxEnemigos:
            return

        # Generamos un número aleatorio constantemente que cada vez que tome un
        # valor arbitrariamente designado (10) spawnearemos un enemigo
        # Este método para decidir cuando aparecer enemigos es raro pero lo
        # escogí para que los enemigos no aparezcan de una forma que sea fácil de
        # predecir para el jugador
        spawnRand = random.randint(0, 250)

        # Apareceremos un enemigo cuando el valor aleatorio sea 10
        if spawnRand == 10:
            spawnRand = 0
            # Generamos aleatoriamente las coordenadas de ese enemigo y las agregamos
            # al diccionario de enemigos junto con el resto de sus datos
            self.enemies[self.numEnemigos] = {
                'coord': [random.randint(20, 750), random.randint(20, 600)],
                'direccion': random.randint(0, 3),
                'counter': 0,
                'estado': 1,
                'deathCounter': 0,
            }
            # Aumentamos la cantidad de enemigos en el nivel
            self.numEnemigos += 1

    # Función que pinta a todos los enemigos en el tablero
    def pintarEnemigo(self, screen, stage, player):
        # Si no hay enemigos no tenemos que pintarlos
        # asi que no hacemos nada en la funcion
        if self.numEnemigos == 0:
            return

        #Si hay por lo menos un enemigo en el tablero,  reproducimos cada cierto tiempo sonidos de zombie para
        # que se haga ambiente
        if self.numEnemigos >= 1 and player.health > 0 and player.killed != player.winGoal:
            self.soundCounter += 1
            if self.soundCounter >= 150:
                self.soundCounter = 0
                sonidoRand = random.randint(0, 3)
                channel.play(zombieAgro[sonidoRand])

        # Primero eliminamos los cadaveres muertos del diccionario
        for k, v in list(self.enemies.items()):
            if v["estado"] == 0 and v["deathCounter"] >= 70:
                del self.enemies[k]

        # Para cada enemigo en el diccionario de enemigos
        for key, value in self.enemies.items():
            # Aumentamos constantemente el valor del contador para saber que tanto tiempo hace que se spawneo
            # el enemigo, si el valor del contador es menor a 80, el enemigo nació hace poco, digamos
            # que es "joven", mientras que el enemigo sea "joven" no lo imprimiremos como un zombie
            # hostil hacia el jugador, sino como una bola de fuego, esto lo hacemos para que los zombies
            # no aparezcan de golpe en el nivel, y le den tiempo al jugador de prepararse para enfrentarlos
            if (value["counter"] < 80):
                #Reproduccion de sonido
                if value["counter"] == 1:
                    channel.play(enemySpawn)
                screen.blit(self.fuego, value["coord"])
                value["counter"] += 1
            # Si estamos frente a un enemigo que NO es joven lo pintamos en su forma zombie
            else:
                # Si el enemigo está vivo
                if value["estado"] == 1:
                    # Decidimos cual set de sprites usaremos en base a la dirección en la que está
                    # mirando el enemigo
                    if value["direccion"] == 0 or value["direccion"] == 1:
                        animacion = self.walking
                    elif value["direccion"] == 2:
                        animacion = self.walkingBack
                    elif value["direccion"] == 3:
                        animacion = self.walkingFront

                    # Cargamos el primer sprite del set
                    walking = pygame.transform.scale(
                        animacion[0], (self.scaleX, self.scaleY))

                    # Usamos el valor del contador para alternar entre los sprites
                    # del set
                    value["counter"] += 1
                    if 100 <= value["counter"] <= 120:
                        walking = pygame.transform.scale(
                            animacion[1], (self.scaleX, self.scaleY))
                        value["counter"] += 1
                    if value["counter"] >= 120:
                        value["counter"] = 80

                    # Pintamos al enemigo con su sprite correspondiente tomando en cuenta la
                    # dirección en la que está mirando
                    if value["direccion"] == 1:
                        walking = pygame.transform.flip(walking, True, False)
                    screen.blit(walking, value["coord"])

                # Si el enemigo está muerto
                else:
                    # Cargamos el sprite de muerte correpondiente a la dirección
                    # en la que está mirando el zombie
                    if value["direccion"] == 0 or value["direccion"] == 1:
                        muerto = self.deadSide
                    elif value["direccion"] == 2:
                        muerto = self.deadBack
                    elif value["direccion"] == 3:
                        muerto = self.deadFront
                    if value["direccion"] == 1:
                        muerto = pygame.transform.flip(muerto, True, False)
                    # Pintamos el cadaver del enemigo
                    muerto = pygame.transform.scale(
                        muerto, (self.scaleX, self.scaleY))
                    screen.blit(muerto, value["coord"])
                    # Incrementamos el contador para llevar control
                    # del tiempo que lleva muerto el enemigo
                    value["deathCounter"] += 1
                    # Si el enemigo lleva muerto mucho tiempo, lo envolvemos en una bola de fuego
                    if (value["deathCounter"] >= 40):
                        screen.blit(self.fuego, value["coord"])
    # Esta función controla el movimiento de todos los enemigos en el nivel
    def move(self, screen, stage, player):

        # Si no hay enemigos no tenemos que moverlos
        # asi que no hacemos nada en la funcion
        if self.numEnemigos == 0:
            return

        # Para cada zombie en el nivel
        for key, value in self.enemies.items():

            # Checamos si el zombie es impactado por una bala del jugador
            if abs(value["coord"][1] - player.balaY) <= 75 and abs(player.balaX - value["coord"][0]) <= 60 and value["counter"] > 65 and player.shoot:
                #Reproduccion de sonido de muerte de zombie
                if value["estado"] == 1:
                    channel.play(zombieDeath)
                # Si el zombie es impactado lo marcamos como muerto
                value["estado"] = 0
                # Sacamos la bala del tablero ya que impacto en el zombie
                player.balaX = 1000
                player.balaY = 1000
                # Marcamos que el jugador acaba de asesinar a un zombie
                player.reproduce = True
                player.killed += 1

             # Definimos las coordenadas a las que buscaran acercarse los zombies
            if player.estado == "FANTASMA":
                metaX = player.cadaverX
                metaY = player.cadaverY
            else:
                metaX = player.playerX
                metaY = player.playerY

            # Checamos si el jugador es atacado por un zombie (Si es fantasma será invulnerable)
            # Creamos una variable de cooldown para que haya frames de invulnerabilidad
            if abs(value["coord"][1] - metaY) <= 50 and abs(metaX - value["coord"][0]) <= 40 and value["counter"] > 65:
                if self.inv == 20:
                    # Reducimos la vida del jugador
                    if player.health >= 1:
                        #Reproducimos sonido de dolor del jugador
                        channel.play(hurt)
                        player.health -= 1
                    # Si el jugador ha perdido toda su vida lo marcamos como muerto
                    if (player.health == 0):
                        if player.estado == "FANTASMA":
                            player.playerX = player.cadaverX
                            player.playerY = player.cadaverY
                        player.estado = "MUERTO"
                self.inv -= 1
                if self.inv <= 0:
                    self.inv = 40

            # Esta sección es la encargada de mover a cada uno de los zombies
            # Solo movemos a los zombies vivos y que no son jovenes
            # En caso de que el jugador sea un fantasma, los zombies buscarán su cadaver
            if value["estado"] == 1 and value["counter"] > 80:
                # Primero cubrimos el caso en el que el jugador esta en su cuerpo humano
                # Caso en el que el zombies alcanza al jugador
                if value["coord"][0] == metaX and value["coord"][1] == metaY:
                    return

                # Caso en el que el zombie está alineado verticalmente con el jugador
                elif value["coord"][0] == metaX:
                    if value["coord"][1] > metaY:
                        value["coord"][1] -= self.velocidad
                        value["direccion"] = 2
                    else:
                        value["coord"][1] += self.velocidad
                        value["direccion"] = 3

                # Caso en el que el zombie está alineado horizontalmente con el jugador
                elif value["coord"][1] == metaY:
                    if value["coord"][0] > metaX:
                        value["coord"][0] -= self.velocidad
                        value["direccion"] = 0
                    else:
                        value["coord"][0] += self.velocidad
                        value["direccion"] = 1

                # Caso en el que el zombie está a la derecha del jugador
                elif value["coord"][0] > metaX:
                    # El zombie está abajo del jugador
                    if value["coord"][1] > metaY:
                        # Lo subimos y lo movemos a la izquierda
                        value["coord"][0] -= self.velocidad
                        value["coord"][1] -= self.velocidad
                        value["direccion"] = 0
                    # Caso en el que el zombie está arriba del jugador
                    else:
                        # Lo bajamos y lo movemos a la izquierda
                        value["coord"][1] += self.velocidad
                        value["coord"][0] -= self.velocidad
                        value["direccion"] = 0
                # Caso en el que el zombie está a la izquierda del jugador
                else:
                    # El zombie está abajo del jugador
                    if value["coord"][1] > metaY:
                        # Lo subimos y lo movemos a la derecha
                        value["coord"][0] += self.velocidad
                        value["coord"][1] -= self.velocidad
                        value["direccion"] = 1
                    # El zombie está arriba del jugador
                    else:
                        # Lo bajamos y lo movemos a la derecha
                        value["coord"][1] += self.velocidad
                        value["coord"][0] += self.velocidad
                        value["direccion"] = 1
