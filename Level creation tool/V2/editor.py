import pygame, os
from settings import *
from extra_functions import * 
from button import Button
from pygame import transform as pyt
from pygame import image as pyi

class PaletteTile(pygame.sprite.Sprite):

    def __init__(self, x, y, palette_number):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        # Set the image as the palette number
        self.image = pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{palette_number}.png"), (64, 64)).convert_alpha()
        # Set the palette number based on the palette number passed in
        self.palette_number = palette_number

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = pygame.display.get_surface()

    def draw(self, x, y):
        # Draw the palette tile onto the screen 
        # Note: These co-ordinates are passed into the method because I want the images to stay at the same position on the screen, but for the rect to move
        self.screen.blit(self.image, (x, y))

class Editor():
    def __init__(self):

        # Set the display as the current display
        self.screen = pygame.display.get_surface()
        self.full_screen = False
        
        # Define the point from which the drawing grid and tiles are drawn
        self.origin_point = pygame.math.Vector2(0, 0)
        
        # Create a transparency surface for the grid to be drawn onto
        self.transparency_surface = pygame.Surface((screen_width, screen_height))

        # Set the alpha level
        self.transparency_surface.set_alpha(75)

        # Set the mouse as not visible initially (This will be changed when the user tries to load an existing tile map)
        pygame.mouse.set_visible(False)

        # ----------------------------------------------------------------------------------------
        # Palette tiles

        # Number to represent what tile the user has selected right now
        self.selected_palette_number = 0

        # Create palette tiles
        self.create_palette_tiles()

        # ----------------------------------------------------------------------------------------
        # Drawing tiles

        # Set the size of the tiles
        self.tile_size = 32 

        # Create a tuple with all the images needed for the tiles
        self.image = self.load_tile_images()
        
        # If there is a text file called "last_tile_map_before_exit"
        if os.path.exists("V2/last_tile_map_before_exit.txt"):
            # Create this attribute so that the history can be restored
            self.load_last_tile_map_before_exit = True

        # Otherwise
        else:
            # Create a new blank tile map / drawing canvas
            self.create_new_blank_tile_map()

        # Attributes used to track whenever changes have been made to the tile map so that progress can be automatically saved
        self.changes_made_to_tile_map = False
        self.automatically_save_progress = False

        # ----------------------------------------------------------------------------------------
        # Buttons
        
        # Create buttons
        self.create_buttons()

        # Record the last time a button was clicked
        self.button_clicked_time = pygame.time.get_ticks()

        # ----------------------------------------------------------------------------------------
        # Palette tiles panel

        # Define the menu x and y co-ordinates (Easier to modify positioning of the menu) and the font used for the tile_map_selected text
        self.palette_tiles_panel_x = 25
        self.palette_tiles_panel_y = 550
        self.palette_tiles_panel_width = 1415
        self.tile_map_selected_text_font = pygame.font.SysFont("Bahnschrift", 15)

        # ----------------------------------------------------------------------------------------
        # Editor states

        self.show_editor = True
        self.show_load_menu = False
        self.show_manage_tile_maps_menu = False

    # ----------------------------------------------------------------------------------------
    # Initial set-up methods
            
    def load_tile_images(self):

        # Find out the number of images in the following directory 
        number_of_images = len(os.listdir("V2/graphics/palette_tiles"))

        # Create a tuple with all of the images inside of the following directory
        images_tuple = tuple( pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{i}.png"), (32, 32)).convert_alpha() for i in range(0, number_of_images) ) 

        # Return the images tuple
        return images_tuple

    def create_palette_tiles(self):

        # Create the palette tiles group
        self.palette_tiles_group = pygame.sprite.Group()

        j = 0 # Keeps track of the current row
        i = 0 # Keeps track of the current item in the row
        palette_tile_count = 0 # Keeps track of the current item in the directory

        # While we haven't made all of the palette tiles in the directory
        while palette_tile_count != len(os.listdir("V2/graphics/palette_tiles")): 

            # If we have reached the maximum amount of palette tiles in each row
            if palette_tile_count % 14 == 0 and palette_tile_count != 0:

                # Go to the next row
                j += 1

                # Reset i, so that the tile is displayed at the start of the row
                i = 0

            # Create a new palette tile and add it to the palette tiles group
            palette_tile = PaletteTile(50 + (100 * i), 550 + 25 + (j * 100), palette_tile_count)
            self.palette_tiles_group.add(palette_tile)
            
            # Increment i index and the palette tile count
            i += 1
            palette_tile_count += 1

    def create_new_blank_tile_map(self):

        # Declare self.tile_map as an empty tile map
        self.tile_map = []
        
        # Declare the tile map as selected as None
        self.tile_map_selected_number = None

        # Calculate the number of lines for x and y
        number_of_lines_x = (screen_width / 2) / 32
        
        # Draws as many tiles as half the resolution can fit. (So in a 1080 resolution, 16 tiles of tile size 32 can fit inside (1080 / 2) resolution)
        number_of_lines_y = ((screen_height / 2) - ( (screen_height / 2) % self.tile_size )) / self.tile_size

        for row in range(0, int(number_of_lines_y)):
            
            # Reset the row of items list for every row
            row_of_items_list = []

            for column in range(0, int(number_of_lines_x)):

                # Create a rect, spacing them out between each other by the tile size
                rect = pygame.Rect((column * self.tile_size), (row * self.tile_size), self.tile_size, self.tile_size)

                # Create a tile containing the rect and palette number (All palette numbers will be set to 0 by default)
                tile = [rect, 0] 

                # Add the tile to the row of items list
                row_of_items_list.append(tile)   
            
            # Add the row of items list to the tile list
            self.tile_map.append(row_of_items_list)

    def create_buttons(self):

        # Create the buttons group
        self.buttons_group = pygame.sprite.Group()

        # Create a list of buttons with all the button images in the buttons directory for the main display
        list_of_buttons = os.listdir("V2/graphics/buttons/editor")

        next_column = 0
        # For all the buttons in the list
        for i in range(0, len(list_of_buttons)):

            # If there are 5 buttons in one column
            if i % 5 == 0 and i != 0:
                # Start drawing buttons at the next column
                next_column = 100

            # Set/ create a new attribute e.g. self.export__tile_map_button, self.extend_drawing_tiles_button, etc.
            # Note: [:-4] removes the ".png" from the attribute name
            setattr(self, f"{list_of_buttons[i][:-4]}", Button(1465 + next_column, 550 + ((i % 5) * 90), pyt.smoothscale(pyi.load(f"V2/graphics/buttons/editor/{list_of_buttons[i]}"), (75, 75)).convert()))

            # Add the new attribute that was just created to the buttons group
            self.buttons_group.add(self.__getattribute__(list_of_buttons[i][:-4]))
        
    # ----------------------------------------------------------------------------------------
    # Interaction methods

    def extend_drawing_tiles_x(self):

        # For each row in the tile list
        for row_count, row in enumerate(self.tile_map):

            # Create a new tile with the palette value, 0, and add it to the end of the row
            row.append([pygame.Rect((len(row)  * self.tile_size), (row_count * self.tile_size), self.tile_size, self.tile_size), 0])
   
    def shrink_drawing_tiles_x(self):
        
        # If the tile list isn't empty
        if len(self.tile_map) > 0:

            # For each row in the tile list
            for row in self.tile_map:
                
                if len(row) > 0:
                    # Remove the last item of the row
                    row.pop()

    def extend_drawing_tiles_y(self):
        
        # Create an empty row (list) which will be added onto the tile map
        row_to_be_added = []
        
        # For the amount of items in one row 
        for i in range(0, len(self.tile_map[0])):

            # Add a new tile to the row, with their own x position (according to the index) all with the same y position
            # Note: The y position should be the number of rows already in the tile map times the tile size
            row_to_be_added.append([pygame.Rect((i * self.tile_size), len(self.tile_map) * self.tile_size, self.tile_size, self.tile_size), 0])

        # Add the row onto the tile map 
        self.tile_map.append(row_to_be_added)

    def shrink_drawing_tiles_y(self):

        # Remove the last row in the tile map
        self.tile_map = self.tile_map[:-1]
            
    def reset_tile_map(self):
        
        # For each row in the tile list
        for row in self.tile_map:
            # For each tile in each row
            for tile in row:
                # Set the palette number to 0
                tile[1] = 0

    def draw_grid(self):

        # Calculate the number of lines for x and y
        number_of_lines_x = screen_width / 32
        
        # Draws as many lines as half the resolution can fit. (So in a 1080 resolution, 16 tiles of tile size 32 can fit inside (1080 / 2) resolution)
        number_of_lines_y = ((screen_height / 2) - ( (screen_height / 2) % self.tile_size )) / self.tile_size

        # Vertical lines
        for i in range(1, int(number_of_lines_x) + 1):
            pygame.draw.line(self.transparency_surface, "white", ((i * 32), 0), ((i * 32), ((screen_height / 2) - ((screen_height / 2) % self.tile_size ))), 2)

        # Horizontal lines
        for j in range(1 , int(number_of_lines_y) + 1): 
            pygame.draw.line(self.transparency_surface, "white", (self.origin_point.x, (j * 32)), (screen_width, (j * 32)), 2)

        # Draw the transparency surface onto the main surface / screen
        self.screen.blit(self.transparency_surface, (0, 0))

    def handle_user_input(self):

        # Retrieve the mouse position
        self.mouse_position = pygame.mouse.get_pos()
        # Define the mouse rect and draw it onto the screen (For collisions with drawing tiles)
        self.mouse_rect = pygame.Rect(((-self.origin_point.x) + self.mouse_position[0], self.mouse_position[1], 1, 1))

        # If the left mouse button is pressed
        if pygame.mouse.get_pressed()[0] == 1:

            # ----------------------------------------------------------------------------------------
            # Changing the drawing tile

            # Check for every tile inside the tile list

            # For each row in the tile list
            for row in self.tile_map:

                # For each item in each row
                for tile in row:

                    # If the mouse rect collides with the tile (tile[0] = tile rect, tile[1] = palette number, tile[0][0] = rect.x, tile[0][1] = rect.y)
                    # Note: I do not use collide rect because then I would need to move all the y positions of the tile rects, which could affect the final tile map
                    if (tile[0][1] - abs(self.origin_point.y) <= self.mouse_rect.y <= tile[0][1] + self.tile_size - abs(self.origin_point.y)) and (tile[0][0] <= self.mouse_rect.x <= tile[0][0] + self.tile_size):

                        # Set the drawing tile's palette number to be the current selected palette tile number
                        tile[1] = self.selected_palette_number

                        # Indicate that changes have been made to the tile map
                        self.changes_made_to_tile_map = True

            # ----------------------------------------------------------------------------------------
            # Changing the palette tile selected

            # Check every palette tile in the palette tile group
            for palette_tile in self.palette_tiles_group:

                # If the mouse rect collides with the palette tile's rect
                if self.mouse_rect.colliderect(palette_tile.rect):

                    # Set the selected palette number to be the palette number of the palette tile that was clicked on
                    self.selected_palette_number = palette_tile.palette_number

            # ----------------------------------------------------------------------------------------
            # Collision with buttons

            # If enough time has passed since the last time a button has been clicked
            if pygame.time.get_ticks() - self.button_clicked_time > 250:

                # If the mouse rect collides with the rect of the extend x drawing tiles button
                if self.mouse_rect.colliderect(self.drawing_tiles_extend_x_button.rect):
                    # Extend the drawing tiles by one column
                    self.extend_drawing_tiles_x()
                
                # If the mouse rect collides with the rect of the shrink x drawing tiles button
                elif self.mouse_rect.colliderect(self.drawing_tiles_shrink_x_button.rect):
                    # Shrink the drawing tiles by one column
                    self.shrink_drawing_tiles_x()

                # If the mouse rect collides with the rect of the extend y drawing tiles button
                elif self.mouse_rect.colliderect(self.drawing_tiles_extend_y_button.rect):
                    # Extend the drawing tiles by one row
                    self.extend_drawing_tiles_y()

                # If the mouse rect collides with the rect of the shrink y drawing tiles button
                elif self.mouse_rect.colliderect(self.drawing_tiles_shrink_y_button.rect):
                    # Shrink the drawing tiles by one row
                    self.shrink_drawing_tiles_y()

                # If the mouse rect collides with the rect of the load tile map button
                elif self.mouse_rect.colliderect(self.load_tile_map_button.rect):
                    
                    # If the text file that stores all of the existing tile maps created is greater than 0 (It means there is at least one tile map inside)
                    if os.path.getsize("V2/existing_tile_maps.txt") > 0:
                        # Stop showing the editor
                        self.show_editor = False
                        # Show the load menu
                        self.show_load_menu = True

                # If the mouse rect collides with the rect of the manage tile maps button
                elif self.mouse_rect.colliderect(self.manage_tile_maps_button.rect):
                        # Stop showing the editor
                        self.show_editor = False
                        # Show the manage tile maps menu
                        self.show_manage_tile_maps_menu = True
                
                # If the mouse rect collides with the rect of the new tile map button
                elif self.mouse_rect.colliderect(self.new_tile_map_button.rect):
                    
                    # Create a new blank tile map, once the user makes changes to this tile map, it will be saved as a unique tile map
                    self.create_new_blank_tile_map()

                # If the mouse rect collides with the rect of the reset tile map button
                elif self.mouse_rect.colliderect(self.reset_tile_map_button.rect):
                    # Reset the tile map
                    self.reset_tile_map()    

                # Record the last time that a button was clicked to be now
                self.button_clicked_time = pygame.time.get_ticks()

        # If the user has let go of the left mouse button / the left mouse button isn't being pressed
        if pygame.mouse.get_pressed()[0] == 0:
            
            # If the user has made changes to the tile map
            if self.changes_made_to_tile_map == True:

                # Set this attribute to True, so that the menu can automatically save the progress
                self.automatically_save_progress = True

                # Set this attribute to False, as the progress has been saved
                self.changes_made_to_tile_map = False

        # ----------------------------------------------------------------------------------------
        # Key presses

        # If the "a" key is being pressed and we aren't trying to go left when we are at (0, ?)
        if pygame.key.get_pressed()[pygame.K_a] and self.origin_point.x != 0:
            # Move the origin point right
            self.origin_point.x += self.tile_size

            # For each palette tile in the palette tiles group
            for palette_tile in self.palette_tiles_group:
                # Move the palette tile rect left 
                palette_tile.rect.x -= self.tile_size

            # For every button in the buttons group
            for button in self.buttons_group:
                # Move the button rect left
                button.rect.x -= self.tile_size

        # If the "d" key is being pressed
        elif pygame.key.get_pressed()[pygame.K_d]:
            
            # Move the origin point left
            self.origin_point.x -= self.tile_size

            # For each palette tile in the palette tiles group
            for palette_tile in self.palette_tiles_group:
                # Move the palette tile rect right
                palette_tile.rect.x += self.tile_size

            # For every button in the buttons group
            for button in self.buttons_group:
                # Move the button rect rightww
                button.rect.x += self.tile_size

        # If the "w" key is being pressed and we aren't trying to go up when we are at (?, 0)
        if pygame.key.get_pressed()[pygame.K_w] and self.origin_point.y != 0:
            # Move the origin point down
            self.origin_point.y += self.tile_size

        # If the "s" key is being pressed 
        elif pygame.key.get_pressed()[pygame.K_s]:
            # Move the origin point up
            self.origin_point.y -= self.tile_size

    def set_new_cursor(self):
        # Draw a circle where the mouse cursor is
        pygame.draw.circle(self.screen, "white", (self.mouse_position[0], self.mouse_position[1]), 15, 15) # Body
        pygame.draw.circle(self.screen, "deepskyblue3", (self.mouse_position[0], self.mouse_position[1]), 15, 3) # Outline 1
        pygame.draw.circle(self.screen, "black", (self.mouse_position[0], self.mouse_position[1]), 15, 1) # Outline 2 

        # Draw the palette tile selected in the middle of the circle
        self.screen.blit(pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{self.selected_palette_number}.png"), (20, 20)).convert_alpha(), (self.mouse_position[0] - (20 / 2), self.mouse_position[1] - (20 / 2) ) )

    def draw_buttons(self):
        
        next_column = 0
        # For every button in the buttons group
        for i, button in enumerate(self.buttons_group):
            
            # If there are 5 buttons in one column
            if i % 5 == 0  and i != 0:
                # Start drawing buttons at the next column
                next_column = 100

            # Draw the button onto the screen
            button.draw(1465 + next_column, 550 + ((i % 5) * 90))

    def draw_tiles(self):

        # For every row in the tile list
        for row in self.tile_map:

            # For each tile in each row
            for tile in row:
                
                # If the y position of the tile minus the origin point's y position is less than the screen height, draw it onto the screen
                # Note: This only draws tiles up to halfway of the screen
                if tile[0][1] - abs(self.origin_point.y) < (screen_height / 2) - self.tile_size:

                    # Draw the appropriate image based on the palette number, at the correct x and y positions from the origin point
                    self.screen.blit(self.image[tile[1]], (self.origin_point.x + tile[0][0], tile[0][1] - abs(self.origin_point.y)))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect

    def draw_palette_tiles(self):

        j = 0 # Keeps track of the current row
        i = 0 # Keeps track of the current item in the row

        # Define the width/height/line thickness for the border of each palette tile
        border_width = 80
        border_height = 80
        border_line_thickness = 3

        # For every palette tile in the palette tiles group
        for palette_tile in self.palette_tiles_group:

            # If we have reached the maximum amount of palette tiles in each row
            if i % 14 == 0 and i != 0:

                # Go to the next row
                j += 1
                # Reset i, so that the tile is displayed at the start of the row
                i = 0

            # Draw an outline and "background" for each palette tile
            pygame.draw.rect(self.screen, "gray33", (50 + (100 * i) - ((border_width - (self.tile_size * 2)) / 2) , 550 + 25 + (j * 100) - ((border_height - (self.tile_size * 2)) / 2), border_width, border_height) , 0)
            pygame.draw.rect(self.screen, "black", (50 + (100 * i) - ((border_width - (self.tile_size * 2)) / 2) , 550 + 25 + (j * 100) - ((border_height - (self.tile_size * 2)) / 2), border_width, border_height) , border_line_thickness)

            # Draw the palette tile onto the screen
            palette_tile.draw(50 + (100 * i), 550 + 25 + (j * 100))

            # Increment i index
            i += 1

    def draw_palette_tiles_panel(self):

        # Declare the palette tiles panel height again (This is because the user may have exited full screen, so the panel would need to re-adjust
        self.palette_tiles_panel_height = self.screen.get_height() - self.palette_tiles_panel_y - 50

        # Body
        pygame.draw.rect(self.screen, "gray20", (self.palette_tiles_panel_x, self.palette_tiles_panel_y, self.palette_tiles_panel_width, self.palette_tiles_panel_height))
        # Outline
        pygame.draw.rect(self.screen, "white", (self.palette_tiles_panel_x, self.palette_tiles_panel_y, self.palette_tiles_panel_width, self.palette_tiles_panel_height), 5)

        # Draw a text indicating the number of the tile map selected. If no tile map has been loaded, the selected number will be "None"
        draw_alpha_text(f"Selected tile map:  {self.tile_map_selected_number}", self.tile_map_selected_text_font, "white", self.palette_tiles_panel_x, self.palette_tiles_panel_y - 25, self.screen, 110)

    def run(self):
        
        # Colour the background
        self.screen.fill("gray17")

        # Draw the palette tiles panel
        self.draw_palette_tiles_panel()

        # Draw the tiles
        self.draw_tiles()   

        # Draw the grid
        self.draw_grid()

        # Draw palette tiles
        self.draw_palette_tiles()

        # Draw buttons
        self.draw_buttons()

        # Handle user input
        self.handle_user_input()

        # Set the cursor image to be the image of the selected palette tile
        self.set_new_cursor()   