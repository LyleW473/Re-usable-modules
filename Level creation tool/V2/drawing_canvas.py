import pygame, sys
from settings import *

# Create drawing tiles
class DrawingTiles():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # Drawing tiles
        self.tile_list = []
        self.palette_number = 0 # Determines what image the drawing tile will display 
        
        # Exporting tile creation
        self.export_tile_list = [] 

        self.origin_point = pygame.math.Vector2(0, 0)

        self.tile_size = 32
 

    def draw_grid(self):

        #pygame.draw.line(self.screen, "black", (0, 900 / 2), (screen_width, 900 / 2))

        number_of_lines_x = (1600 / 2) / 32
        number_of_lines_y = (928 / 2) / 32

        for i in range(1, int(number_of_lines_x) + 1):
            pygame.draw.line(self.screen, "red", (self.origin_point.x + (i * 64), 0), (self.origin_point.x + (i * 64), 900 / 2), 1)

        for j in range(1, int(number_of_lines_y) + 1):
            pygame.draw.line(self.screen, "white", (self.origin_point.x, (j * 32)), (screen_width, (j * 32)), 1)


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
        
        
    # def create_drawing_tiles(self, number_of_lines, tile_size):
    #     for row in range(0, number_of_lines):
    #         for column in range(0, number_of_lines):
    #             # Create a rect, spacing them out between each other by the tile size
    #             rect = pygame.Rect(250 + (column * tile_size), 250 + (row * tile_size), tile_size, tile_size)
    #             # Create a tile containing the rect and the palette number (the palette number will be changed later on)
    #             tile = [rect, self.palette_number] 
    #             # Add the tile to the tile list
    #             self.tile_list.append(tile)       

    #     # For every tile in the tile list
    #     for tile in self.tile_list:
    #         # Draw the appropriate image based on the palette number, at the correct x and y positions
    #         self.screen.blit(self.image[tile[1]], (tile[0][0], tile[0][1]))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect


    def run(self):
        print(self.origin_point)
        # Draw the grid
        self.draw_grid()

        # self.create_drawing_tiles()

        # Handle user input
        self.handle_user_input()



