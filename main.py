import pygame
import classes
import music
import window


screen = window.setWindow()
player = classes.Player()  
stage = classes.Stage()


#Main game loop
running = True
while running:                                
   
    for event in pygame.event.get():
        #Game controls
        player.movimientos(event, screen)
        #Terminate game when window is closed
        if event.type == pygame.QUIT:
                running = False
                
    #Game Graphics     
    stage.pintarFondo(stage.fondos, screen)
    player.pintarJugador(player.estado, screen)  
    player.HUD(screen)
    pygame.display.update()
