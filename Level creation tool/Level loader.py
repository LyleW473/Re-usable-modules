# Import modules
import pygame, sys
from pygame.locals import *


# Initialise pygame
pygame.init()

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Sample tilemap
test_tilemap = [ # Columns
                [5,2,0,0,0],  # Rows
                [7,1,5,0,0],  
                [3,1,9,0,6], 
                [6,0,5,0,9], 
                [8,0,7,0,0],]

class TileMap():
    def __init__(self, map):
        self.tile_list = []
        
        # Look inside the tile map that has been passed into the instance of the TileMap.
        for row_count, row in enumerate(map):
            for item_count, item in enumerate(row):
                # Check what the item is inside the tile map and 
                if item == 1:
                    image = pygame.transform.scale(pygame.image.load("1.png"), (200,200))
                    image_rect = image.get_rect()
                    image_rect.x = (item_count * 200)
                    image_rect.y = (row_count * 200)

                    tile_info = (image, image_rect)
                    self.tile_list.append(tile_info)


                if item == 2:
                    image = pygame.transform.scale(pygame.image.load("2.png"), (200,200))
                    image_rect = image.get_rect()
                    image_rect.x = (item_count * 200)
                    image_rect.y = (row_count * 200)

                    # Create a tuple containing the image and the x and y co-ordinates
                    tile_info = (image, image_rect) # The image and the image's rectangular x and y position
                    self.tile_list.append(tile_info)
                
    def draw(self):
        # For every tile inside the tile list, draw the tile's image at the (x, y) co-ordinate given
        for tile_info in self.tile_list:
            screen.blit(tile_info[0], tile_info[1]) # [0] = image, [1] = image_rect


# Instances
world = TileMap(test_tilemap)


def draw_grid():
    for line in range(0, 5):
        pygame.draw.line(screen, WHITE, (0, line * 200), (screen_width, line * 200))
        pygame.draw.line(screen, WHITE, (line * 200, 0), (line * 200, screen_height))

# Main loop
run = True
while run:
    # Fill the background with blue
    screen.fill(BLUE)

    # Draw the world
    world.draw()

    # Draw the grid to visualise tile squares
    draw_grid()


    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
