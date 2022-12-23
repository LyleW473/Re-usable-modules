import pygame, sys
from settings import *
from pygame import transform as pyt
from pygame import image as pyi

# Create drawing tiles
class DrawingTiles():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.origin_point = pygame.math.Vector2(0, 0) # The point where the drawing grid and tiles are drawn from
        # Drawing tiles
        self.tile_list = []
        # Number to represent what a tile is
        self.palette_number = 0
        # Set the size of the tiles
        self.tile_size = 32 
        # Create a tuple with all the images needed for the tiles
        self.image = ( pyt.scale(pyi.load("V2/graphics/empty.png"), (32, 32)), pyt.scale(pyi.load("V2/graphics/1.png"), (32, 32)) , pyt.scale(pyi.load("V2/graphics/2.png"), (32, 32)) )
        # Create the initial drawing tiles
        self.create_drawing_tiles()

    def draw_grid(self):

        # Calculate the number of lines for x and y
        number_of_lines_x = (1600 / 2) / 32
        number_of_lines_y = (900 / 2) / 32

        # Vertical lines
        for i in range(1, int(number_of_lines_x) + 1):
            pygame.draw.line(self.screen, "white", (self.origin_point.x + (i * 32), 0), (self.origin_point.x + (i * 32), 896 / 2), 1)

        # Horizontal lines
        for j in range(1, int(number_of_lines_y) + 1):
            pygame.draw.line(self.screen, "black", (self.origin_point.x, (j * 32)), (screen_width, (j * 32)), 1)


    def handle_user_input(self):
        # Retrieve the mouse position
        self.mouse_position = pygame.mouse.get_pos()

        # If the left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            print("left click") 

        # If the "a" key is being pressed
        if pygame.key.get_pressed()[pygame.K_a]:
            # Move the origin point right
            self.origin_point.x += 5
        
        # If the "d" key is being pressed
        elif pygame.key.get_pressed()[pygame.K_d]:
            # Move the origin point left
            self.origin_point.x -= 5
        
        
    def create_drawing_tiles(self):
        # Calculate the number of lines for x and y
        number_of_lines_x = (1600 / 2) / 32
        number_of_lines_y = (900 / 2) / 32

        for row in range(0, int(number_of_lines_x)):
            for column in range(0, int(number_of_lines_y)):

                # Create a rect, spacing them out between each other by the tile size
                rect = pygame.Rect((row * self.tile_size), (column * self.tile_size), self.tile_size, self.tile_size)

                # Create a tile containing the rect and the palette number (the palette number will be changed later on)
                tile = [rect, self.palette_number] 

                # Add the tile to the tile list
                self.tile_list.append(tile)       

    
    def draw_tiles(self):
        
        # For every tile in the tile list
        for tile in self.tile_list:
            
            # Draw the appropriate image based on the palette number, at the correct x and y positions from the origin point
            self.screen.blit(self.image[tile[1]], (self.origin_point.x + tile[0][0], self.origin_point.y + tile[0][1]))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect


    def run(self):

        # Draw the tiles onto the screen
        self.draw_tiles()

        # Draw the grid
        self.draw_grid()

        # Handle user input
        self.handle_user_input()



