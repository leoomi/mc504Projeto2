import pygame, sys
from pygame.locals import *
pygame.init()
from GameObject import *

screen = pygame.display.set_mode((400, 300))
screen.fill((255, 255, 255))

pygame.display.set_caption('Banheiro Unissex')

testTex = pygame.image.load('penguin.png')
fpsClock = pygame.time.Clock()
group = pygame.sprite.Group()

background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill((255, 255, 255))

GameObject.groups = group
test = GameObject((400, 0), (100, 100), testTex)   #test purposes

while True: # main game loop
    time = fpsClock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    group.clear(screen, background)
    group.update(time/1000.0)
    group.draw(screen)

    pygame.display.update()
    