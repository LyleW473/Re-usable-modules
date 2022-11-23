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
GREY = (93,93,93)

# Fonts
export_list_font = pygame.font.SysFont('Bebas Neue', 30)

# Load images
eraser_image = pygame.image.load("-1.png").convert()
first_image = pygame.image.load("1.png").convert_alpha()
second_image = pygame.image.load("2.png").convert_alpha()
empty_image = pygame.image.load("empty.png").convert()


# Variables
left_mouse_button_held_down = False
border_rect = (250, 250, 500, 500) # x, y, width, height
initial_drawing_tiles = True  # Used to draw the starting drawing tiles


tile_size = 100 # The tile size for the drawing tiles
number_of_lines = int(500 / tile_size) # Number of lines to draw for the grid
selected_palette_tile = 0 # 0 = nothing,  -1 = Eraser, 1 = Tile 1, 2 = Tile 2, 3 = Tile 3, 

cursor_colour = WHITE # Default cursor colour is white, it will change one a tool is pressed

# Exporting
export_list = [] # The list that will be replaced by the tile list
show_exported_text = False # Determines whether we show the exported text or not

# Scaled images

# "Drawing tiles" images
empty_icon = pygame.transform.scale(empty_image, (tile_size, tile_size))
first_palette_tile_icon = pygame.transform.scale(first_image, (tile_size, tile_size))
second_palette_tile_icon = pygame.transform.scale(second_image, (tile_size, tile_size))


""" 
The drawing board is 500 x 500

Ask to declare a tile size, based on the tile size the number of 


Make the mouse stuff a class thing

 """


def draw_grid(number_of_lines, tile_size):
    for line in range(0, number_of_lines):
        pygame.draw.line(screen, RED, (250, 250 + (line * tile_size)), (750, 250 + (line * tile_size)))
        pygame.draw.line(screen, GREEN, (250 + (line * tile_size), 250), (250 + (line * tile_size) , 750))

def draw_text(text, font, text_colour, x, y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (x, y))

# Create drawing tiles
class DrawingTiles():
    def __init__(self):
        # Drawing tiles
        self.tile_list = []
        self.palette_number = 0 # Determines what image the drawing tile will display 
        self.image = (empty_icon, first_palette_tile_icon, second_palette_tile_icon) # The image can be one of 3 images. It is a tuple because they will never change. These will be selected using a palette number.
        
        # Exporting tile creation
        self.export_tile_list = [] 

    def create_drawing_tiles(self, number_of_lines, tile_size):
        for row in range(0, number_of_lines):
            for column in range(0, number_of_lines):
                # Create a rect, spacing them out between each other by the tile size
                rect = Rect(250 + (column * tile_size), 250 + (row * tile_size), tile_size, tile_size)
                # Create a tile containing the rect and the palette number (the palette number will be changed later on)
                tile = [rect, self.palette_number] 
                # Add the tile to the tile list
                self.tile_list.append(tile)

    def draw(self):
        # For every tile in the tile list
        for tile in self.tile_list:
            # Draw the appropriate image based on the palette number, at the correct x and y positions
            screen.blit(self.image[tile[1]], (tile[0][0], tile[0][1]))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect
        

    def export(self, number_of_lines):
        temp_tile_list = []
        export_tile_list = []
        item_count = 0

        # Note: The number_of_lines is the same as the number of tiles there will be in each row e

        # Converting the drawing tile list into an exportable list

        # For every tile in the tile list
        for tile in self.tile_list:
            # If the item count isn't equal to the number of items inside that row
            if item_count < number_of_lines:
                # Append the palette number to a temporary list
                temp_tile_list.append(tile[1]) 
                # Increment the item count
                item_count += 1

            # If it is equal to the number of items in that row
            if item_count == number_of_lines:
                # Once separated into the correct amount of items per row, add it to the export tile list
                export_tile_list.append(temp_tile_list)
                # Empty the temporary tile list to take another x amount of items
                temp_tile_list = []
                # Reset the item count
                item_count = 0   

        return export_tile_list


class PaletteTiles(pygame.sprite.Sprite):
    def __init__(self, image, x, y, palette_number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.palette_number = palette_number 

    def draw(self):
        screen.blit(self.image, (self.rect))


# Groups
palette_tiles_group = pygame.sprite.Group()

# Instances

# Palette that the player uses to draw onto the canvas
eraser_tile = PaletteTiles(eraser_image, 100, 800, -1)
first_tile = PaletteTiles(first_image, 300, 800, 1)
second_tile = PaletteTiles(second_image, 500, 800, 2)

palette_tiles_group.add(eraser_tile)
palette_tiles_group.add(first_tile)
palette_tiles_group.add(second_tile)

# Drawing tiles instance
drawing_tiles = DrawingTiles()



# Main loop
run = True
while run:
    screen.fill(GREY)

    # Draw border rect
    pygame.draw.rect(screen, WHITE, border_rect, 2)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # DRAWING TILES

    # Create the starting drawing tiles
    if initial_drawing_tiles == True:
        drawing_tiles.create_drawing_tiles(number_of_lines, tile_size)
        initial_drawing_tiles = False


    # Draw the drawing tiles
    drawing_tiles.draw()

    # Drawing palette tiles
    palette_tiles_group.draw(screen)

    # Draw the grid (temporary)
    #draw_grid(number_of_lines, tile_size)
    
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Hide default cursor
    #pygame.mouse.set_visible(False)

    # Find the current mouse position
    mouse_position = pygame.mouse.get_pos()
    mouse_position_rect = Rect((mouse_position[0], mouse_position[1], 20, 20))
    pygame.draw.rect(screen, cursor_colour, mouse_position_rect, 0)

    # Changing colour of the cursor
    # Eraser
    if selected_palette_tile == -1:
        cursor_colour = RED
    # Tile 1
    elif selected_palette_tile == 1:
        cursor_colour = GREEN
    # Tile 2
    elif selected_palette_tile == 2:
        cursor_colour = BLUE

    # If the left mouse button is held down / clicked 
    if left_mouse_button_held_down == True:

        # For all drawing tiles
        for drawing_tile in drawing_tiles.tile_list:

            # Check for collision with the mouse  (between the tile rect and the mouse position rect)
            if drawing_tile[0].colliderect(mouse_position_rect):
    
                # Eraser tool
                if selected_palette_tile == -1:
                    # Set the tile's palette number as the default tile (this will change the tile image)
                    drawing_tile[1] = 0 
                    

                # Tile 1
                if selected_palette_tile == 1:
                    # Set the tile's palette number as tile 1 (this will change the tile image)
                    drawing_tile[1] = 1

                # Tile 2
                if selected_palette_tile == 2:
                    # Set the tile's palette number as tile 2 (this will change the tile image)
                    drawing_tile[1] = 2


        # For all palette tiles
        for palette_tile in palette_tiles_group:
            
            # Check for a collision with the mouse
            if palette_tile.rect.colliderect(mouse_position_rect):

                # Set the selected tile to be the one that will be drawn if the player clicks on a drawing tile
                selected_palette_tile = palette_tile.palette_number

    # If the user has just exported their list
    if show_exported_text == True:
        # If it hasn't been 5 seconds since the list has been exported
        if (pygame.time.get_ticks() - exported_time) < 5000:
            # Draw the export list text
            draw_text("List has been exported", export_list_font, WHITE, 50, 50)
        else:
            # Set this variable back to False
            show_exported_text = False





    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()

        # Single clicks
        # # Check if the mouse button has been pressed
        # if event.type == MOUSEBUTTONDOWN:
        #     # Check if the mouse button clicked was the left click
        #     if event.button == 1: # (1 = left, 2 = middle, 3 = right, 4 = scroll up, 5 = scrolldown)
        #         print("clicked")

        # Check if the left mouse button is being held
        if pygame.mouse.get_pressed()[0] == True:
            left_mouse_button_held_down = True
        if pygame.mouse.get_pressed()[0] == False:
            left_mouse_button_held_down = False

        if event.type == KEYDOWN:
            # If the "r" key is pressed
            if event.key == K_r:
                # Reset the drawing tiles list
                drawing_tiles.tile_list = []
                # Create plain drawing tiles again
                drawing_tiles.create_drawing_tiles(number_of_lines, tile_size)

            if event.key == K_e:
                # Export file
                export_list = drawing_tiles.export(number_of_lines)
                print(export_list)
                exported_time = pygame.time.get_ticks()
                show_exported_text = True

    pygame.display.update()
