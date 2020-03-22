import pygame

windowX = 800
windowY = 800

def setWindow():
    pygame.init()
    screen = pygame.display.set_mode((windowX,windowY))
    pygame.display.set_caption("AfterLife")
    icon = pygame.image.load("character/front.png")
    pygame.display.set_icon(icon)
    pygame.key.set_repeat(1,10)
    return screen