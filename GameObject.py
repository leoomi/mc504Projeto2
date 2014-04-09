import pygame
import threading

class GameObject(pygame.sprite.Sprite):
    def __init__(self, initialPos, size, texture):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speed = [80, 80]
        self.destination = [250, 250]
        self.image = pygame.Surface((100, 100))
        self.image = texture
        self.rect = self.image.get_rect()
        self.image.convert_alpha()
        
    def update(self, deltaTime):
        self.movement(deltaTime)
    
    def movement(self, deltaTime):
        self.rect.x = self.rect.x + deltaTime*self.speed[0]
        self.rect.y = self.rect.y + deltaTime*self.speed[1]

        if(self.rect.x > self.destination[0]):
            self.rect.x = self.destination[0]

        if(self.rect.y > self.destination[1]):
            self.rect.y = self.destination[1]
