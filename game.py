import pygame
import classes
import window


def AfterLife():

    # Screen setup
    screen = window.setWindow()
    player = classes.Player()
    stage = classes.Stage()
    enemy = classes.Enemy()

    # Screen update rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Screen update rate
        clock.tick(60)

        # Event listener loop
        for event in pygame.event.get():
            # Game controls
            player.movimientos(event, stage)
            # Terminate game when window is closed
            if event.type == pygame.QUIT:
                running = False

        # Game Graphics
        stage.pintarFondo(stage.fondos, screen)
        enemy.spawn(stage, player)
        enemy.pintarEnemigo(screen, stage, player)
        player.pintarJugador(player.estado, screen, stage)
        enemy.move(screen, stage, player)
        player.HUD(screen, stage, enemy)
        pygame.display.update()
