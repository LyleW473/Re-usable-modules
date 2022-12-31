import pygame
from settings import * 

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tile_map = None, tile_map_number = None, purpose = None):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.screen = pygame.display.get_surface()

        # Store the tile map that is passed to the object
        self.stored_tile_map = tile_map

        # Store the tile map number
        self.stored_tile_map_number = tile_map_number

        # Select the purpose of the button
        self.purpose = purpose
        

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))