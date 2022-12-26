import pygame, os, string, sys
from settings import *
from extra_functions import * 
from pygame import transform as pyt
from pygame import image as pyi

class PaletteTile(pygame.sprite.Sprite):

    def __init__(self, x, y, palette_number):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        # Set the image as the palette number
        self.image = pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{palette_number}.png"), (64, 64))
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

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Inherit from pygame's sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = pyt.scale(image, (64, 64)) # Scale all buttons to this size
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
    
class DrawingTiles():
    def __init__(self):

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.origin_point = pygame.math.Vector2(0, 0) # The point where the drawing grid and tiles are drawn from
        
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

        # Create a new tile map (A new tile map is created by default upon loading the program)
        self.create_new_tile_map()

        # ----------------------------------------------------------------------------------------
        # Buttons
        
        # Create buttons
        self.create_buttons()

        # Record the last time a button was clicked
        self.button_clicked_time = pygame.time.get_ticks()

    # ----------------------------------------------------------------------------------------
    # Initial set-up methods
    def loading_tile_map_input(self):
        
        # Set the mouse cursor as visible when asking for user input when loading a tile map
        pygame.mouse.set_visible(True)
    
        existing_tile_maps_dict =  {} # Holds all of the existing tile maps
        tile_map_count = 0 # Holds the number of tile maps saved in the file

        # ------------------------------------------------
        # Find out the number of tile maps and save it to the dictionary

        # Open the existing tile maps file 
        with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:

            # For each line in the tile maps file
            for line in existing_tile_maps_file.readlines():

                # If the line starts with "[[", it means this line contains the tile map
                if line.startswith("[["):

                    # Increment the tile map count
                    tile_map_count += 1
                    
                    # Create a new key:value pair in the existing tile maps dictionary, remove the \n at the end of each line
                    existing_tile_maps_dict[tile_map_count] = line.strip("\n")

        # ------------------------------------------------
        # Handling user input for choosing tile map

        # Define an empty user input string, font used, the user input box and a variable which tracks whether the user entered an invalid tile map
        user_input_string = ""
        user_input_font = pygame.font.SysFont("Bahnschrift", 40)
        user_input_rectangle = pygame.Rect((screen_width / 2) - 110, (screen_height / 2) - 30, 200, 60)
        invalid_input = False

        # Continuously ask for user input 
        while True: 
            
            # Fill the screen with grey
            self.screen.fill("gray17") 

            # Display the instructions onto the screen
            draw_text("Please enter a tile map", user_input_font, "white", user_input_rectangle.x - 100, user_input_rectangle.y - 60, self.screen)

            # Display the user input string onto the screen
            draw_text(user_input_string, user_input_font, "white", user_input_rectangle.x + 10, user_input_rectangle.y + 10, self.screen)

            # Display the number of tile maps text onto the screen
            draw_text(f"There are {len(existing_tile_maps_dict)} tile maps.", user_input_font, "dodgerblue4", user_input_rectangle.x - 90, user_input_rectangle.y - 160, self.screen)

            # Draw a rectangle for the user input 
            pygame.draw.rect(self.screen, "black", user_input_rectangle, 5)
            
            # If the user entered an invalid tile map
            if invalid_input == True:

                # Display the invalid text onto the screen for 1 second
                if pygame.time.get_ticks() - invalid_input_time < 1000:
                    draw_text(f"Tilemap {int(user_input_string)} does not exist.", user_input_font, "red", user_input_rectangle.x - 110, user_input_rectangle.y + 90, self.screen)
                
                # Once the second has passed
                else:
                    # Reset the user input string
                    user_input_string = ""

                    # Reset the invalid_input variable
                    invalid_input = False

            # ------------------------------------------------
            # Event handler
            for event in pygame.event.get():
                
                # If the user pressed a key
                if event.type == pygame.KEYDOWN:

                    # If the key that was pressed is a number and the tile map number selected is a single digit number
                    if event.unicode in string.digits and len(user_input_string) < 1:
                        # Concatenate the digit onto user_input_string
                        user_input_string += event.unicode

                    # If the user pressed the backspace key
                    if event.key == pygame.K_BACKSPACE and invalid_input == False:
                        # Remove the last item of the text and the user hasn't recently entered an invalid tile map
                        user_input_string = user_input_string[:-1]

                    # If the user pressed the return / enter key and the user input string is not empty and the user hasn't recently entered an invalid tile map
                    if event.key == pygame.K_RETURN and len(user_input_string) > 0 and invalid_input == False:

                        # If the tile map selected is a key in the existing tile maps dictionary
                        if int(user_input_string) in existing_tile_maps_dict.keys():

                            # Set the mouse cursor invisible again
                            pygame.mouse.set_visible(False)

                            # Output a message in the terminal to indicate that the tile map selected is being loaded
                            print(f"Loading tilemap {int(user_input_string)}...")

                            # Return the tile map (this is fed into the load_existing_tile_map method)
                            return existing_tile_maps_dict[int(user_input_string)]


                        # If the tile map selected isn't a key in the existing tile maps dictionary
                        else:
                            # Set the invalid input variable to True
                            invalid_input = True

                            # Record the time that the user got the 
                            invalid_input_time = pygame.time.get_ticks()

                # If the exit button was pressed
                if event.type == pygame.QUIT:
                    # Close the program
                    pygame.quit()
                    sys.exit()

            # Update display
            pygame.display.update()

    def load_existing_tile_map(self, tile_map):

        # Reset self.tile_list so that if the user tried loading multiple tilemaps, only one tile map is displayed at a time
        self.tile_list = []

        # Set the string_tile_list as the tile map selected by the user from the loading_tile_map_input method
        string_tile_list = tile_map

        # Save the tile map selected as an attribute 
        # Note: This is so that when the user is given the choice to save this as a new tile map or to overwrite the existing tile map, we know which tile map to replace in the text file if they choose to overwrite the existing tile map
        self.existing_tile_map_selected = tile_map

        # ----------------------------------------------------------------------------------------
        # Cleaning the string

        # Remove the first and last 2 brackets
        string_tile_list = string_tile_list[2:-2]

        # After each sublist, separate them using a #
        string_tile_list = string_tile_list.replace("], [", "#")

        # Separate each item in each sub list with an exclamation mark (this is because some tiles may have double digit palette numbers)
        string_tile_list = string_tile_list.replace(", ", "!")

        # Create lists of strings containing the tile numbers
        string_tile_list = string_tile_list.split("#")

        # Create a new string tile list
        new_string_tile_list = []

        # ----------------------------------------------------------------------------------------
        # Converting back into a list (each digit is still a string, but this will be converted to an integer later)

        # For each sub list in the string tile list
        for sub_list in string_tile_list:

            # Create a new sub list splitting each sublist wherever there is an exclamation mark
            new_sub_list = sub_list.split("!")

            # Add the new sub list to the new string tile list
            new_string_tile_list.append(new_sub_list)
       
        # ----------------------------------------------------------------------------------------
        # Converting back into a tile list of rectangles (The actual tile map)

        # For each row in the new string tile list
        for row_index, row in enumerate(new_string_tile_list):
    
            # Reset the row of items list for every row
            row_of_items_list = []  

            # For each item in the row
            for item_count, item in enumerate(row):
                    
                # Create a rect, spacing them out between each other by the tile size
                rect = pygame.Rect((item_count * self.tile_size), (row_index * self.tile_size), self.tile_size, self.tile_size)

                # Create a tile containing the rect and palette number of the item, converting the item into an int (as it should be a string at this stage)
                tile = [rect, int(item)]

                # Add the tile to the row of items list
                row_of_items_list.append(tile)

            # Add the row of items list to the tile list
            self.tile_list.append(row_of_items_list)
        
        # Output a message in the terminal to indicate that the tile map selected has finished loading
        print("Loading complete.")
            
    def load_tile_images(self):

        # Find out the number of images in the following directory 
        number_of_images = len(os.listdir("V2/graphics/palette_tiles"))

        # Create a tuple with all of the images inside of the following directory
        images_tuple = tuple( pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{i}.png"), (32, 32)) for i in range(0, number_of_images) ) 

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
            palette_tile = PaletteTile(50 + (100 * i), 500 + (j * 100), palette_tile_count)
            self.palette_tiles_group.add(palette_tile)
            
            # Increment i index and the palette tile count
            i += 1
            palette_tile_count += 1

    def create_new_tile_map(self):

        # Reset self.tile_list so that if the user tried loading multiple tilemaps, only one tile map is displayed at a time
        self.tile_list = []

        # Calculate the number of lines for x and y
        number_of_lines_x = (screen_width / 2) / 32
        number_of_lines_y = (screen_height / 2) / 32

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
            self.tile_list.append(row_of_items_list)

    def create_buttons(self):

        # Create the buttons group
        self.buttons_group = pygame.sprite.Group()

        # Create a list of buttons with all the button images in the buttons directory
        list_of_buttons = os.listdir("V2/graphics/buttons")

        # For all the buttons in the list
        for i in range(0, len(list_of_buttons)):

            # Set/ create a new attribute e.g. self.export__tile_map_button, self.extend_drawing_tiles_button, etc.
            setattr(self, f"{list_of_buttons[i][:-4]}", Button(1500, 475 + (i * 80), pyi.load(f"V2/graphics/buttons/{list_of_buttons[i]}")) ) # [:-4] removes the ".png" from the attribute name

            # Add the new attribute that was just created to the buttons group
            self.buttons_group.add(self.__getattribute__(list_of_buttons[i][:-4]))
        
    # ----------------------------------------------------------------------------------------
    # Interaction methods

    def extend_drawing_tiles(self):

        # For each row in the tile list
        for row_count, row in enumerate(self.tile_list):

            # Create a new tile with the palette value, 0, and add it to the end of the row
            row.append([pygame.Rect( ( (len(row)  * self.tile_size), (row_count * self.tile_size), self.tile_size, self.tile_size)), 0])
   
    def shrink_drawing_tiles(self):
        
        # If the tile list isn't empty
        if len(self.tile_list) > 0:

            # For each row in the tile list
            for row in self.tile_list:
                
                if len(row) > 0:
                    # Remove the last item of the row
                    row.pop()

    def save_tile_map(self):

        # List which will hold all the rows of items inside the tile map
        tile_map_to_be_saved = []

        # For each row in the tile list
        for row_count, row in enumerate(self.tile_list):

            # Create a new row of items list
            row_of_items_list = []

            # For all items in the row
            for i in range(0, len(row)):

                # Add the palette number of the tile to the row of items list
                row_of_items_list.append(self.tile_list[row_count][i][1])

            # Add the row of items list to the the tile map to be saved
            tile_map_to_be_saved.append(row_of_items_list)

        # Variable that stores the user's choice of whether to overwrite the existing tile map selected ro 
        save_as_new_tile_map = False

        # If the user has chosen to overwrite the existing tile map selected
        if save_as_new_tile_map == False:

                # Open the file to read the contents
                with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:
                    # Read the contents of the file and save it to a variable
                    existing_tile_maps_file_content = existing_tile_maps_file.read()

                    # Replace the old tile map stored in the text with the tile map to be saved
                    existing_tile_maps_file_content = existing_tile_maps_file_content.replace(self.existing_tile_map_selected, str(tile_map_to_be_saved))

                    # Set the existing tile map selected as the saved tile map
                    self.existing_tile_map_selected = str(tile_map_to_be_saved)

                # Open the file to write the contents
                with open("V2/existing_tile_maps.txt", "w") as existing_tile_maps_file:
                    # Write the changes made to the existing tile maps file
                    existing_tile_maps_file.write(existing_tile_maps_file_content)

        # If the user has chosen to save the current tile map as a new tile map
        else:
            # Open the existing tile maps and append the current list of tiles (only palette numbers)
            with open("V2/existing_tile_maps.txt", "a") as existing_tile_maps_file:

                # Add a line break at the end of each tile map save
                existing_tile_maps_file.write(str(tile_map_to_be_saved) + "\n")

    def reset_tile_map(self):
        # For each row in the tile list
        for row in self.tile_list:
            # For each tile in each row
            for tile in row:
                # Set the palette number to 0
                tile[1] = 0

    def draw_grid(self):

        # Calculate the number of lines for x and y
        number_of_lines_x = screen_width / 32
        number_of_lines_y = (screen_height / 2) / 32

        # Vertical lines
        for i in range(1, int(number_of_lines_x) + 1):
            pygame.draw.line(self.transparency_surface, "white", ((i * 32), 0), ((i * 32), 896 / 2), 2)

        # Horizontal lines
        for j in range(1, int(number_of_lines_y) + 1):
            pygame.draw.line(self.transparency_surface, "white", (self.origin_point.x, (j * 32)), (screen_width, (j * 32)), 2)

        # Draw the transparency surface onto the main surface / screen
        self.screen.blit(self.transparency_surface, (0, 0))

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

            # For each row in the tile list
            for row in self.tile_list:

                # For each item in each row
                for tile in row:

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

            # ----------------------------------------------------------------------------------------
            # Collision with buttons

            # If enough time has passed since the last time a button has been clicked
            if pygame.time.get_ticks() - self.button_clicked_time > 500:

                # If the mouse rect collides with the rect of the extend drawing tiles button
                if self.mouse_rect.colliderect(self.drawing_tiles_extend_button.rect):
                    # Extend the drawing tiles by one column
                    self.extend_drawing_tiles()
                
                # If the mouse rect collides with the rect of the shrink drawing tiles button
                if self.mouse_rect.colliderect(self.drawing_tiles_shrink_button.rect):
                    # Shrink the drawing tiles by one column
                    self.shrink_drawing_tiles()

                # If the mouse rect collides with the rect of the load tile map button
                if self.mouse_rect.colliderect(self.load_tile_map_button.rect):
                    # If the text file that stores all of the existing tile maps created is greater than 0 (It means there is at least one tile map inside)
                    if os.path.getsize("V2/existing_tile_maps.txt") > 0:
                        # Call the loading_existing tile map method with the parameter set as the tile map from the input stage 
                        self.load_existing_tile_map(tile_map = self.loading_tile_map_input())

                # If the mouse rect collides with the rect of the save tile map button
                if self.mouse_rect.colliderect(self.save_tile_map_button.rect):
                    # Save the tile map
                    self.save_tile_map()    

                # If the mouse rect collides with the rect of the reset tile map button
                if self.mouse_rect.colliderect(self.reset_tile_map_button.rect):
                    # Reset the tile map
                    self.reset_tile_map()    

                # Record the last time that a button was clicked to be now
                self.button_clicked_time = pygame.time.get_ticks()

        # If the "a" key is being pressed and we aren't trying to go left, beyond the origin point
        if pygame.key.get_pressed()[pygame.K_a] and self.origin_point.x < 0:

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
                # Move the button rect right
                button.rect.x += self.tile_size

    def set_new_cursor(self):
        # Draw a circle where the mouse cursor is
        pygame.draw.circle(self.screen, "white", (self.mouse_position[0], self.mouse_position[1]), 15, 15) # Body
        pygame.draw.circle(self.screen, "deepskyblue3", (self.mouse_position[0], self.mouse_position[1]), 15, 3) # Outline 1
        pygame.draw.circle(self.screen, "black", (self.mouse_position[0], self.mouse_position[1]), 15, 1) # Outline 2 

        # Draw the palette tile selected in the middle of the circle
        self.screen.blit(pyt.scale(pyi.load(f"V2/graphics/palette_tiles/{self.selected_palette_number}.png"), (20, 20)), (self.mouse_position[0] - (20 / 2), self.mouse_position[1] - (20 / 2) ) )

    def draw_buttons(self):

        # For every button in the buttons group
        for i, button in enumerate(self.buttons_group):
            # Draw the button onto the screen
            button.draw(1500, 475 + (i * 80))

    def draw_tiles(self):

        # For every row in the tile list
        for row in self.tile_list:

            # For each tile in each row
            for tile in row:

                # Draw the appropriate image based on the palette number, at the correct x and y positions from the origin point
                self.screen.blit(self.image[tile[1]], (self.origin_point.x + tile[0][0], self.origin_point.y + tile[0][1]))  # tile[1] =  palette number, tile[0][0] = The x co-ordinate of the rect, tile[0][1] = the y co-ordinate of the rect

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
            pygame.draw.rect(self.screen, "gray33", (50 + (100 * i) - ((border_width - (self.tile_size * 2)) / 2) , 500 + (j * 100) - ((border_height - (self.tile_size * 2)) / 2), border_width, border_height) , 0)
            pygame.draw.rect(self.screen, "black", (50 + (100 * i) - ((border_width - (self.tile_size * 2)) / 2) , 500 + (j * 100) - ((border_height - (self.tile_size * 2)) / 2), border_width, border_height) , border_line_thickness)

            # Draw the palette tile onto the screen
            palette_tile.draw(50 + (100 * i), 500 + (j * 100))

            # Increment i index
            i += 1

    def draw_tiles_menu(self):
        # Body
        pygame.draw.rect(self.screen, "gray20", (25, 475, 1425, 400))
        # Outline
        pygame.draw.rect(self.screen, "white", (25, 475, 1425, 400), 5)

    def run(self):

        # Draw the tiles menu
        self.draw_tiles_menu()

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