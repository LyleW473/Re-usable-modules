import pygame, sys
from settings import *
from pygame import transform as pyt
from pygame import image as pyi

class PaletteTile(pygame.sprite.Sprite):

    def __init__(self, x, y, palette_number):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        # Set the image as the palette number
        self.image = pyt.scale(pyi.load(f"V2/graphics/{palette_number}.png"), (64, 64))
        # Set the palette number based on the palette number passed in
        self.palette_number = palette_number

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw(self, x, y):
        # Draw the palette tile onto the screen 
        # Note: These co-ordinates are passed into the method because I want the images to stay at the same position on the screen, but for the rect to move
        self.screen.blit(self.image, (x, y))

# Create drawing tiles
class DrawingTiles():
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.origin_point = pygame.math.Vector2(0, 0) # The point where the drawing grid and tiles are drawn from
        
        # ----------------------------------------------------------------------------------------
        # Palette tiles

        # Number to represent what tile the user has selected right now
        self.selected_palette_number = 0

        # Palette tiles group
        self.palette_tiles_group = pygame.sprite.Group()

        # Create palette tiles
        for i in range(0, 2 + 1):
            # Create a new palette tile and add it to the palette tiles group
            palette_tile = PaletteTile(50 + (100 * i), 600, i)
            self.palette_tiles_group.add(palette_tile)

        # ----------------------------------------------------------------------------------------
        # Drawing tiles
        self.tile_list = []
        # Set the size of the tiles
        self.tile_size = 32 
        # Create a tuple with all the images needed for the tiles
        self.image = ( pyt.scale(pyi.load("V2/graphics/empty.png"), (32, 32)), pyt.scale(pyi.load("V2/graphics/1.png"), (32, 32)) , pyt.scale(pyi.load("V2/graphics/2.png"), (32, 32)) )
        # Create the initial drawing tiles
        self.create_drawing_tiles()

        # Set mouse as not visible
        pygame.mouse.set_visible(False)

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

        # Define the mouse rect and draw it onto the screen (For collisions with drawing tiles)
        self.mouse_rect = pygame.Rect(((-self.origin_point.x) + self.mouse_position[0], self.mouse_position[1], 20, 20))

        # If the left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            # ----------------------------------------------------------------------------------------
            # Changing the drawing tile

            # Check for every tile inside the tile list
            for tile in self.tile_list:

                # If the mouse rect collides with the tile rect (tile[0] = tile rect, tile[1] = palette number )
                if self.mouse_rect.colliderect(tile[0]):
                    print(f"Clicked on {tile[0]}")

                    # Set the drawing tile's palette number to be the current selected palette tile number
                    tile[1] = self.selected_palette_number

            # ----------------------------------------------------------------------------------------
            # Changing the palette tile selected

            # Check every palette tile in the palette tile group
            for palette_tile in self.palette_tiles_group:

                # If the mouse rect collides with the palette tile's rect
                if self.mouse_rect.colliderect(palette_tile.rect):
                    print(f"Clicked on {palette_tile}, palette_number = {palette_tile.palette_number}")

                    # Set the selected palette number to be the palette number of the palette tile that was clicked on
                    self.selected_palette_number = palette_tile.palette_number

        # If the "a" key is being pressed
        if pygame.key.get_pressed()[pygame.K_a]:

            # Move the origin point right
            self.origin_point.x += 5

            # For each palette tile in the palette tiles group
            for palette_tile in self.palette_tiles_group:
                # Move the palette tile rect left 
                palette_tile.rect.x -= 5
                

        # If the "d" key is being pressed
        elif pygame.key.get_pressed()[pygame.K_d]:
            
            # Move the origin point left
            self.origin_point.x -= 5

            # For each palette tile in the palette tiles group
            for palette_tile in self.palette_tiles_group:
                # Move the palette tile rect right
                palette_tile.rect.x += 5


    def set_new_cursor(self):
        # Draw a circle where the mouse cursor is
        pygame.draw.circle(self.screen, "white", (self.mouse_position[0], self.mouse_position[1]), 15, 15) # Body
        pygame.draw.circle(self.screen, "deepskyblue3", (self.mouse_position[0], self.mouse_position[1]), 15, 3) # Outline 1
        pygame.draw.circle(self.screen, "black", (self.mouse_position[0], self.mouse_position[1]), 15, 1) # Outline 2 

        # Draw the palette tile selected in the middle of the circle
        self.screen.blit(pyt.scale(pyi.load(f"V2/graphics/{self.selected_palette_number}.png"), (20, 20)), (self.mouse_position[0] - (20 / 2), self.mouse_position[1] - (20 / 2) ) )

    def create_drawing_tiles(self):
        # Calculate the number of lines for x and y
        number_of_lines_x = (1600 / 2) / 32
        number_of_lines_y = (900 / 2) / 32

        for row in range(0, int(number_of_lines_x)):
            for column in range(0, int(number_of_lines_y)):

                # Create a rect, spacing them out between each other by the tile size
                rect = pygame.Rect((row * self.tile_size), (column * self.tile_size), self.tile_size, self.tile_size)

                # Create a tile containing the rect and palette number (All palette numbers will be set to 0 by default)
                tile = [rect, 0] 

                # Add the tile to the tile list
                self.tile_list.append(tile)       

    def draw_tiles(self):
        
        # For every tile in the tile list
        for tile in self.tile_list:

            # Draw the appropriate image based on the palette number, at the correct x and y positions from the origin point
            self.screen.blit(self.image[tile[1]], (self.origin_point.x + tile[0][0], self.origin_point.y + tile[0][1]))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect

    def draw_palette_tiles(self):

        # For every palette tile in the palette tiles group
        for i, palette_tile in enumerate(self.palette_tiles_group):
            # Draw the palette tile onto the screen
            palette_tile.draw(50 + (100 * i), 600)

    def run(self):

        # Draw the tiles onto the screen
        self.draw_tiles()

        # Draw the grid
        self.draw_grid()    

        # Draw palette tiles
        self.draw_palette_tiles()

        # Handle user input
        self.handle_user_input()

        # Set the cursor image to be the image of the selected palette tile
        self.set_new_cursor()   