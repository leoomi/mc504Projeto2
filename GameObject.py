import pygame
import threading

class GameObject(pygame.sprite.Sprite):
    def __init__(self, initialPos, size, texture):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((100, 100))
        self.image = texture
        self.rect = self.image.get_rect()
        self.image.convert_alpha()
    def update(self):
        self.rect.x = self.rect.x + 1

def diagonal(sprite, destination):
    
    
