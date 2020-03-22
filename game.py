import pygame
import classes
import window

def AfterLife():

    #Screen setup
    screen = window.setWindow()
    player = classes.Player()  
    stage = classes.Stage()
    #Main game loop
    running = True
    while running:                                
    
        for event in pygame.event.get():
            #Game controls
            player.movimientos(event, stage)
            #Terminate game when window is closed
            if event.type == pygame.QUIT:
                    running = False
                    
        #Game Graphics     
        stage.pintarFondo(stage.fondos, screen)
        player.pintarJugador(player.estado, screen, stage)  
        player.HUD(screen, stage)
        pygame.display.update()