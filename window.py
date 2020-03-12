import pygame

def setWindow():
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("AfterLife")
    icon = pygame.image.load("character/bigsadboy.png")
    pygame.display.set_icon(icon)
    pygame.key.set_repeat(1,10)
    return screen