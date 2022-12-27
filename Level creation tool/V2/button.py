import pygame
from settings import * 

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))