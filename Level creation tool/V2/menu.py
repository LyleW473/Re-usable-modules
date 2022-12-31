import pygame, sys, string
from settings import *
from button import Button
from extra_functions import *
from editor import Editor
from pygame import image as pyi
from pygame import transform as pyt

class Menu:

    def __init__(self):
        
        # Set the display as the current display
        self.screen = pygame.display.get_surface()
        self.full_screen = True

        # Holds all the existing tile maps
        self.existing_tile_maps_dict = {}

        # Define the point from which the drawing grid and tiles are drawn
        self.origin_point = pygame.math.Vector2(0, 0)

        # Define the point from which the buttons inside the manage tile maps menu are drawn from
        self.menu_origin_point = pygame.math.Vector2(0, 0)
        # -------------------------------------------
        # Create the editor

        self.editor = Editor()

        # ------------------------------------------- 
        # MENUS

        self.manage_tile_maps_menu_updated = False
        self.load_tile_maps_menu_updated = False

        # ------------------------------------------- 
        # Load menu

        # Define an empty user input string, font and the user input box
        self.user_input_string = ""
        self.user_input_font = pygame.font.SysFont("Bahnschrift", 40)
        self.user_input_rectangle = pygame.Rect((screen_width / 2) - 110, (screen_height / 2) - 30, 200, 60)

        # Attributes used to detect whenever the user inputted an invalid tile map, e.g. 50 when there are only 20 tile maps.
        self.invalid_input = False
        self.invalid_input_time = 0

        # Buttons
        self.return_to_editor_button = Button((screen_width / 2) - 250, self.menu_origin_point.y + self.user_input_rectangle.y + 400, pyi.load("V2/graphics/buttons/menu/return_to_editor_button.png").convert())

        # ------------------------------------------- 
        # Manage tile maps menu 
        
        # Font
        self.manage_tm_font_1 = pygame.font.SysFont("Bahnschrift", 30)
        self.manage_tm_font_2 = pygame.font.SysFont("Bahnschrift", 20)

        # Images
        self.select_button_image = pyi.load("V2/graphics/buttons/menu/select_button.png").convert()
        self.swap_button_image =  pyi.load("V2/graphics/buttons/menu/swap_button.png").convert()
        self.delete_button_image = pyi.load("V2/graphics/buttons/menu/delete_button.png").convert()
        self.deselect_button_image = pyi.load("V2/graphics/buttons/menu/deselect_button.png").convert()
        self.undo_button_image = pyi.load("V2/graphics/buttons/menu/undo_button.png").convert()

        # Selecting / Swapping
        self.first_selected_tile_map_for_swapping = None
        self.second_selected_tile_map_for_swapping = None
        self.swap_made_time = 0
        
        # Deleting 
        self.deletion_complete_time = 0

        # Undo-ing
        # Create an undo button
        self.undo_button = Button(abs(self.origin_point.x) + (screen_width - self.undo_button_image.get_width() - 100), (self.screen.get_height() - self.undo_button_image.get_height()) - 50, self.undo_button_image, purpose = "Undo")
        self.action_performed = False
        self.undo_made_time = 0
    # ----------------------------------------------------------------------------------------
    # Helper methods

    def mouse_position_updating(self):
        # Used to update the mouse position and mouse rect
        
        # Retrieve the mouse position
        self.mouse_position = pygame.mouse.get_pos()

        # Define the mouse rect and draw it onto the screen (For collisions with drawing tiles)
        self.mouse_rect = pygame.Rect(((-self.origin_point.x) + self.mouse_position[0], self.mouse_position[1], 1, 1))

    def find_existing_tile_maps(self):
        # Finds out the number of tile maps in the text file and updates the existing tile maps dictionary with the contents

        # Reset the existing tile maps dictionary 
        self.existing_tile_maps_dict = {}

        tile_map_count = 0 # Holds the number of tile maps saved in the file

        # Open the existing tile maps file 
        with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:

            # For each line in the tile maps file
            for line in existing_tile_maps_file.readlines():

                # If the line starts with "[[", it means this line contains the tile map
                if line.startswith("[["):

                    # Increment the tile map count
                    tile_map_count += 1
                    
                    # Create a new key:value pair in the existing tile maps dictionary, remove the \n at the end of each line
                    self.existing_tile_maps_dict[tile_map_count] = line.strip("\n")          

    def update_menus(self):
        
        # Update the origin point for the menus (to be the same as the editor origin point so that the button rects are accurate)
        self.origin_point = self.editor.origin_point

        # Find out the number of tile maps and save it to the dictionary
        self.find_existing_tile_maps()

        # Set / update the button positions (so that the rects are positioned properly in the case that the user moved the camera right or the user has exited full screen)
        self.return_to_editor_button.rect.x = abs(self.origin_point.x) + (screen_width / 2) - 250
        self.return_to_editor_button.rect.y = self.screen.get_height() - self.return_to_editor_button.image.get_height() - 50

        # Set the mouse cursor as visible when asking for user input when loading a tile map
        pygame.mouse.set_visible(True)

    def execute_common_menu_functionality(self):
        
        # Fill the screen with grey
        self.screen.fill("gray17")

        # Update the mouse position and mouse rect
        self.mouse_position_updating()

        # Draw the return to editor button
        self.return_to_editor_button.draw((screen_width / 2) - 250, self.screen.get_height() - self.return_to_editor_button.image.get_height() - 50)

    # ----------------------------------------------------------------------------------------
    # Loading methods

    def loading_tile_map_input(self):
        # Note: The rest of the code involving interaction with the user input rectangle is within the event loop method
        # Note 2: Common functionality with other menus is within the self.execute_common_menu_functionality method

        # ------------------------------------------------
        # Menu display

        # Display the instructions onto the screen
        draw_text("Please enter a tile map", self.user_input_font, "white", self.user_input_rectangle.x - 100, self.user_input_rectangle.y - 60, self.screen)

        # Display the user input string onto the screen
        draw_text(self.user_input_string, self.user_input_font, "white", self.user_input_rectangle.x + 10, self.user_input_rectangle.y + 10, self.screen)

        # Display the number of tile maps text onto the screen
        draw_text(f"There are {len(self.existing_tile_maps_dict)} tile maps.", self.user_input_font, "dodgerblue4", self.user_input_rectangle.x - 90, self.user_input_rectangle.y - 160, self.screen)

        # Draw a rectangle for the user input 
        pygame.draw.rect(self.screen, "black", self.user_input_rectangle, 5)

        # If the user entered an invalid tile map
        if self.invalid_input == True:

            # Display the invalid text onto the screen for 1 second
            if pygame.time.get_ticks() - self.invalid_input_time < 1000:
                draw_text(f"Tilemap {int(self.user_input_string)} does not exist.", self.user_input_font, "red", self.user_input_rectangle.x - 110, self.user_input_rectangle.y + 90, self.screen)
            
            # Once the second has passed
            else:
                # Reset the user input string
                self.user_input_string = ""

                # Reset the invalid_input variable
                self.invalid_input = False

        # ------------------------------------------------
        # Handle mouse input

        # If the user has pressed the left click
        if pygame.mouse.get_pressed()[0]:

            # If the mouse rect collides with the rect of the save as new tile map button
            if self.mouse_rect.colliderect(self.return_to_editor_button.rect):

                # Set the mouse cursor invisible again
                pygame.mouse.set_visible(False)

                # Show the editor and stop showing the load menu
                self.editor.show_editor = True
                self.editor.show_load_menu = False

                # Reset the attribute that states whether the load menu has been updated
                self.load_tile_maps_menu_updated = False
                
                # Reset the user input string (So that the next time the user enters the load menu, the string will be empty)
                self.user_input_string = ""

                # Exit the method
                return None
     
    def load_existing_tile_map(self, tile_map):

        # Create an empty tile list to hold the final tile map
        tile_list = []

        # Set the string_tile_list as the tile map selected by the user from the loading_tile_map_input method (or the tile map from the dictionary)
        string_tile_list = tile_map

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
                rect = pygame.Rect((item_count * self.editor.tile_size), (row_index * self.editor.tile_size), self.editor.tile_size, self.editor.tile_size)

                # Create a tile containing the rect and palette number of the item, converting the item into an int (as it should be a string at this stage)
                tile = [rect, int(item)]

                # Add the tile to the row of items list
                row_of_items_list.append(tile)

            # Add the row of items list to the tile list
            tile_list.append(row_of_items_list)
        
        # Output a message in the terminal to indicate that the tile map selected has finished loading
        print("Loading complete.")

        # Set the editor's tile map to be the same as the one that was just loaded 
        self.editor.tile_map = tile_list

    # ----------------------------------------------------------------------------------------
    # Saving methods

    def save_tile_map(self, automatically_save_variable = None):
        
        # Set the tile list the same as the one in the editor
        tile_list = self.editor.tile_map

        # ----------------------------------------------------------------------------------------
        # Automatic saving

        # If the automatically save variable has been set to True and the user has selected an existing tile map
        if automatically_save_variable == True and self.editor.tile_map_selected_number != None:

            # Save the progress onto the current tile map selected
            save_as_new_tile_map = False

            # Output a message saying that the progress has been saved onto the current selected tile map
            print("Progress has been saved.")

        # If the automatically save variable has been set to True but the user hasn't selected an existing tile map
        elif automatically_save_variable == True and self.editor.tile_map_selected_number == None:

            # Save the progress as a new tile map
            save_as_new_tile_map = True

        # ----------------------------------------------------------------------------------------
        # Convert the current tile map into a tile map of its palette numbers

        # List which will hold all the rows of items inside the tile map
        tile_map_to_be_saved = []

        # For each row in the tile list
        for row_count, row in enumerate(tile_list):

            # Create a new row of items list
            row_of_items_list = []

            # For all items in the row
            for i in range(0, len(row)):

                # Add the palette number of the tile to the row of items list
                row_of_items_list.append(tile_list[row_count][i][1])

            # Add the row of items list to the the tile map to be saved
            tile_map_to_be_saved.append(row_of_items_list)

        # ----------------------------------------------------------------------------------------
        # Save the tile map according to the user's choice

        # If the user has chosen to overwrite the existing tile map selected
        if save_as_new_tile_map == False:

                # Open the file to read the contents
                with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:
                    # Read the contents of the file and save it to a variable
                    existing_tile_maps_file_content = existing_tile_maps_file.read()

                    # Replace the old tile map stored in the text with the tile map to be saved
                    existing_tile_maps_file_content = existing_tile_maps_file_content.replace(self.existing_tile_maps_dict[self.editor.tile_map_selected_number], str(tile_map_to_be_saved))

                    # Set the existing tile map selected as the saved tile map
                    self.existing_tile_maps_dict[self.editor.tile_map_selected_number] = str(tile_map_to_be_saved)

                # Open the file to write the contents
                with open("V2/existing_tile_maps.txt", "w") as existing_tile_maps_file:
                    # Write the changes made to the existing tile maps file
                    existing_tile_maps_file.write(existing_tile_maps_file_content)

                # Output a message in the terminal
                print("Saved onto existing tile map")

        # If the user has chosen to save the current tile map as a new tile map
        elif save_as_new_tile_map == True:
            # Open the existing tile maps and append the current list of tiles (only palette numbers)
            with open("V2/existing_tile_maps.txt", "a") as existing_tile_maps_file:

                # Add a line break at the end of each tile map save
                existing_tile_maps_file.write(str(tile_map_to_be_saved) + "\n")

                # Output a message in the terminal
                print("Saved as new file.")

        # Update the existing tile maps dictionary
        # Note: This is because inside the main program, if there were previously no tile maps and you tried saving a new tile map, an empty dictionary would be referenced
        self.find_existing_tile_maps()

        # If the automatically save variable is True and a new tile map was created, it means that the system automatically saved progress without an existing tile map being selected
        if automatically_save_variable == True and save_as_new_tile_map == True:
            return "Unsuccessful"

    def automatically_save_progress(self):
        
        # Automatically save the tile map
        status = self.save_tile_map(automatically_save_variable = True)

        # If status is "Unsuccessful", it means that the user tried saving changes made onto a blank canvas, so a new tile map was created. Therefore, the tile map should be loaded up.
        if status == "Unsuccessful":
            """ 
            - It loads up the last tile map inside the dictionary (because this should be the recently created tile map).
            - The tile map passed in should be a list containing the tile map, and the number of the tile map inside the file (which should be the last tile map in the dictionary)

            """
            # Load up the recently created tile map (The last tile map in the text file)
            self.load_existing_tile_map(tile_map = self.existing_tile_maps_dict[len(self.existing_tile_maps_dict)] )

            # Set the number of the tile map selected as the last tile map in the text file
            self.editor.tile_map_selected_number = len(self.existing_tile_maps_dict)

        # Set this attribute back to False so that we stop automatically saving progress for now
        self.editor.automatically_save_progress = False

    # ----------------------------------------------------------------------------------------
    # Managing tile maps menu methods

    # -----------------------------------------
    # Helper methods

    def create_buttons(self):

        # Define a variable which will increment, drawing the buttons at the next page if there are 8 on one page already
        next_page_y = 0

        # Create a group for the buttons inside the manage tile maps
        self.manage_tile_maps_buttons_group = pygame.sprite.Group()
        
        # Create a dictionary for the "Tilemap: i" text positions
        self.text_positions_dict = {}

        # Do this for all tile maps inside the existing tile maps dictionary
        for i in range(0, len(self.existing_tile_maps_dict)):

            # If there are 8 buttons on one page already
            if i % 8 == 0 and i != 0:   
                # Start drawing buttons on the next page
                next_page_y += (screen_height - 800) 

            # Create a select, swap and delete button for each tile map
            # Store a tile map inside each button ([i + 1] because tile maps are not set as zero indexed) and assign a purpose to the button
            select_button = Button(abs(self.origin_point.x) + 250, 100 + (i * 100) + next_page_y, self.select_button_image, tile_map = self.existing_tile_maps_dict[i + 1], purpose = "Select", tile_map_number = i + 1)
            swap_button = Button(abs(self.origin_point.x) + 250 + 200 + 100, 100 + (i * 100) + next_page_y, self.swap_button_image, tile_map = self.existing_tile_maps_dict[i + 1], purpose = "Swap", tile_map_number = i + 1)
            delete_button = Button(abs(self.origin_point.x) + 250 + 200 + 200 + 100 + 100, 100 + (i * 100) + next_page_y, self.delete_button_image, tile_map = self.existing_tile_maps_dict[i + 1], purpose = "Delete", tile_map_number = i + 1)

            # Add the buttons to the group
            self.manage_tile_maps_buttons_group.add(select_button)
            self.manage_tile_maps_buttons_group.add(swap_button)
            self.manage_tile_maps_buttons_group.add(delete_button)

            # Add the co-ordinates where the "Tilemap: i" text will be drawn at 
            self.text_positions_dict[i] = [50, 110 + (i * 100) + next_page_y]

    def draw_buttons(self):

        # For each button in the manage tile maps buttons group
        for button in self.manage_tile_maps_buttons_group:
            # Draw the button at these positions
            button.draw(button.rect.x - abs(self.origin_point.x), button.rect.y)
        
        # Draw the undo button
        self.undo_button.draw((screen_width - self.undo_button_image.get_width() - 100), (self.screen.get_height() - self.undo_button_image.get_height()) - 50)
    
    def calculate_pages(self):

        # Calculate the number of pages there are
        remainder = len(self.existing_tile_maps_dict) % 8 

        # If the remainder is greater than 0
        if remainder > 0:
            # The number of pages would be the number of tile maps divided by 8 and an extra page
            # If there were 22 tile maps, we would need 3 pages)
            self.num_of_pages = int(len(self.existing_tile_maps_dict) / 8) + 1

        # If the remainder is 0
        elif remainder == 0:

            # If there are no tile maps, there should be 1 page
            if len(self.existing_tile_maps_dict) == 0:
                self.num_of_pages = 1

            # If there are tile maps
            else:
                # The number of pages would be the number of tile maps divided by 8
                # If there was 16 tile maps, we would need 2 pages
                self.num_of_pages = int(len(self.existing_tile_maps_dict) / 8)      

    def draw_manage_tile_maps_menu_text(self):

        # Draw text displaying what page the user is on
        draw_text(f"Current page: {self.current_page}", self.manage_tm_font_1, "white", 50, self.screen.get_height() - 80, self.screen)

        # ----------------------------------------------------------------------------------------
        # Draw a text displaying which tile map number it is

        # For each tile map
        for tile_map_number, position_list in self.text_positions_dict.items():
            
            # If the y-position of the text is within the boundaries of the current page we are on
            if self.menu_origin_point.y <= position_list[1] < self.menu_origin_point.y + screen_height:

                # Draw at position y MOD screen_height because these we are drawing them straight onto the screen, not from the origin
                draw_text(f"Tilemap: {tile_map_number + 1}", self.manage_tm_font_1, "white", position_list[0], position_list[1] % screen_height, self.screen)

        # ----------------------------------------------------------------------------------------
        # Draw a text to indicate that the swap has been made, if it hasn't been 2 seconds since the swap has been made
        if pygame.time.get_ticks() - self.swap_made_time < 2000 and self.swap_made_time != 0:
            draw_text(f"Swap has been made!", self.manage_tm_font_2, "chartreuse2", (screen_width / 2) - 100, 50, self.screen)

        # ----------------------------------------------------------------------------------------
        # Draw a text to indicate that the deletion was successful, if it hasn't been 2 seconds since the tile map was deleted
        if pygame.time.get_ticks() - self.deletion_complete_time < 2000 and self.deletion_complete_time != 0:
            draw_text(f"Tilemap successfully deleted!", self.manage_tm_font_2, "chartreuse2", (screen_width / 2) - 125, 50, self.screen)

        # ----------------------------------------------------------------------------------------
        # Draw a text to indicate that the undo was successful, if it hasn't been 2 seconds since the undo was completed
        if pygame.time.get_ticks() - self.undo_made_time < 2000 and self.undo_made_time != 0:
            draw_text(f"Changes undone!", self.manage_tm_font_2, "aqua", (screen_width / 2) - 80, 50, self.screen)

    def refresh_manage_tile_maps_menu(self):

        # Update the existing tile maps dictionary with the new version of the tile maps text file
        self.find_existing_tile_maps()

        # Create the buttons again, (this is because if e.g. the 2nd tile map was deleted, the 3rd tile map before deletion would now be the 2nd tile map (every tile map moves down)
        self.create_buttons()

        # Calculate the number of pages again and go back to the previous page if we are over the maximum number of pages
        self.calculate_pages()

    def save_text_file_for_undo(self):

        # In case that the user did not mean to swap the tile maps / delete the tile map, save a copy of the current version of text file
        with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:
            self.back_up_text_file = existing_tile_maps_file.read()    

    # -----------------------------------------
    # Interaction methods

    def select_tile_map_for_swapping(self, button):
        
        # Set the selected tile map for swapping to be the tile map that was selected (200 x 50)
        self.first_selected_tile_map_for_swapping = button.stored_tile_map

        # Set the select button's image to be the deselect button image
        button.image = self.deselect_button_image

    def deselect_tile_map_for_swapping(self, button):

        # Set the selected tile map for swapping back to None
        self.first_selected_tile_map_for_swapping = None

        # Set the image of the button back to the select button image
        button.image = self.select_button_image

    def swap_tile_maps(self, second_button):

        # ----------------------------------------------------------------------------------------
        # Save the current version of the text file in case the user wants to undo their last action
        self.save_text_file_for_undo()

        # ----------------------------------------------------------------------------------------
        # Swapping tile maps

        # Set the second selected tile map for swapping to be the stored tile map of the second button that was clicked
        self.second_selected_tile_map_for_swapping = second_button.stored_tile_map

        # Open the file to read the contents
        with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:

            # Read the contents of the file and save it to a variable
            existing_tile_maps_file_content = existing_tile_maps_file.read()

            # ----------------------------------------------------------------------------------------
            # Swapping lines

            # Replace the first selected tile map with a temporary string
            existing_tile_maps_file_content = existing_tile_maps_file_content.replace(self.first_selected_tile_map_for_swapping, "?")

            # Replace the second selected tile map with the first selected tile map
            existing_tile_maps_file_content = existing_tile_maps_file_content.replace(self.second_selected_tile_map_for_swapping, self.first_selected_tile_map_for_swapping)
            
            # Replace the temporary string with the second selected tile map
            existing_tile_maps_file_content = existing_tile_maps_file_content.replace("?", self.second_selected_tile_map_for_swapping)

        # Open the file to write the contents
        with open("V2/existing_tile_maps.txt", "w") as existing_tile_maps_file:
            # Write the changes made to the existing tile maps file
            existing_tile_maps_file.write(existing_tile_maps_file_content)

        # Reset the second selected tile map for swapping
        self.second_selected_tile_map_for_swapping = None

        # Output a message in the terminal
        print("Swap has been made")

        # ----------------------------------------------------------------------------------------
        # Manually loading the tile map (in case that the user was on one of the tile maps when the swap was made)

        if self.editor.tile_map_selected_number != None:

            # Update the existing tile maps dictionary with the new version of the tile maps
            self.find_existing_tile_maps()

            # Load the correct tile map using the selected tile map number
            self.load_existing_tile_map(tile_map = self.existing_tile_maps_dict[self.editor.tile_map_selected_number])

    def delete_tile_map(self, tile_map_number):

        # ----------------------------------------------------------------------------------------
        # Save the current version of the text file in case the user wants to undo their last action
        self.save_text_file_for_undo()

        # ----------------------------------------------------------------------------------------
        # Deleting the tile map

        # Declare an empty string which will hold all the tile maps except for the one selected for deletion
        existing_tile_maps_file_content = ""

        # Open the file to read the contents
        with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:

            # Iterate through each line inside the text file
            for line_number, text_tile_map in enumerate(existing_tile_maps_file.readlines()):

                # If the line number we are on is not the same as the tile map number (Line number is compared because there may be tile maps with the same layout so we should not compare tile maps)
                # Note: line_number + 1, because the tile maps are stored non-zero indexed (first tile map starts at index 1)
                if line_number + 1 != tile_map_number:
                    # Add the tile map to the content we will update the text file with
                    existing_tile_maps_file_content += text_tile_map

        # Open the file to write the contents
        with open("V2/existing_tile_maps.txt", "w") as existing_tile_maps_file:
            # Write the changes made to the existing tile maps file
            existing_tile_maps_file.write(existing_tile_maps_file_content)  

        # Set the time that the tile map was deleted to be now
        self.deletion_complete_time = pygame.time.get_ticks()

        # Output a message in the terminal stating that the tile map has been deleted
        print(f"Deleted tile map {tile_map_number}!")

        # ----------------------------------------------------------------------------------------
        # Additional checks / features

        # Refresh the menu

        self.refresh_manage_tile_maps_menu()

        # If the user is now on a page with no buttons on it
        if self.current_page > self.num_of_pages:
            # Go back to the previous page
            self.current_page -= 1
            self.menu_origin_point.y -= screen_height

        # Calculate the amount we need to subtract from the button rectangle so that all button rects are aligned according to what page the user is currently on
        realignment_y = (self.current_page - 1) * screen_height
        for button in self.manage_tile_maps_buttons_group:
            button.rect.y -= realignment_y

        # ----------------------------------------------------------------------------------------
        # - Manually loading the tile map in the situation the user was on the tile map that they selected for deletion 
        # - Manually loading the same tile map in the situation that the user was on a tile map greater than the tile map selected for deletion
        # - Creating a new blank tile map in the situation that there are no more tile maps

        # User was on the tile map selected for deletion or if the user was on a tile map greater than the tile map selected for deletion (E.g. On tile map 34, when tile map 1 was deleted)
        if self.editor.tile_map_selected_number != None and self.editor.tile_map_selected_number >= tile_map_number:
            
            # If the user wasn't on the very first tile map 
            if self.editor.tile_map_selected_number > 1:

                # Go to the tile map before the one that was deleted (e.g. if 24 was deleted, load in tile map 23)
                # If the user was on tile map 23 when tile map 1 was deleted, all tile maps shift down by 1, so tile map 23 will now be tile map 22
                self.editor.tile_map_selected_number -= 1
                
                # Output a message in the terminal saying that we are loading the tile map
                print(f"Loading tilemap {self.editor.tile_map_selected_number}...")

                # Load the correct tile map using the selected tile map number
                self.load_existing_tile_map(tile_map = self.existing_tile_maps_dict[self.editor.tile_map_selected_number])

            # If the user was on the first tile map
            elif self.editor.tile_map_selected_number == 1:

                # Create a new tile map (The selected tile map number is automatically reset back to "None")
                self.editor.create_new_blank_tile_map()
                
                # Output a message in the terminal saying that we created a blank canvas
                print("Created a blank tile map! There are no more tile maps to delete!")

    def manage_tile_maps_menu(self):
        # Note: Interaction with the buttons is inside the event loop

        # ------------------------------------------------
        # Main display

        # Draw the buttons for this menu
        self.draw_buttons()

        # Draw all of the text for this menu
        self.draw_manage_tile_maps_menu_text()
        pygame.draw.line(self.screen, "white", (screen_width / 2, 0), (screen_width / 2, screen_height), 1)
    def undo_action(self):
        # For deletion and swapping, reverse the changes by going back to the previous version of the text file

        # Open the file to write the contents
        with open("V2/existing_tile_maps.txt", "w") as existing_tile_maps_file:
            # Reverse the changes
            existing_tile_maps_file.write(self.back_up_text_file)

        # Record the time that the undo was made
        self.undo_made_time = pygame.time.get_ticks()

        # Output a message stating that the undo was performed
        print(f"Changes undone!")

        # Reset action performed back to False
        self.action_performed = False

        # Refresh the menu
        self.refresh_manage_tile_maps_menu()

        # Calculate the amount we need to subtract from the button rectangle so that all button rects are aligned according to what page the user is currently on
        realignment_y = (self.current_page - 1) * screen_height
        for button in self.manage_tile_maps_buttons_group:
            button.rect.y -= realignment_y
        # ----------------------------------------------------------------------------------------
        # Manually loading the tile map (in case that the user was on one of the tile maps when the swap was made)

        if self.editor.tile_map_selected_number != None:

            # Update the existing tile maps dictionary with the new version of the tile maps
            self.find_existing_tile_maps()

            # Load the correct tile map using the selected tile map number
            self.load_existing_tile_map(tile_map = self.existing_tile_maps_dict[self.editor.tile_map_selected_number])

    # ----------------------------------------------------------------------------------------
    # Main program methods

    def event_loop(self):

        # Event handler
        for event in pygame.event.get():

            # If the exit button was pressed
            if event.type == pygame.QUIT:
                # Close the program
                pygame.quit()
                sys.exit()         

            # If the user pressed a key
            if event.type == pygame.KEYDOWN:

                # -------------------------------------------------
                # Universal events
                
                # If the user pressed the "Escape" key
                if event.key == pygame.K_ESCAPE:

                    # Exit the program
                    pygame.quit()
                    sys.exit()
                
                # If the user pressed the "f" key
                if event.key == pygame.K_f:

                    # Changing from full screen to windowed
                    if self.full_screen == True:
                        
                        # Set back to windowed mode
                        self.screen = pygame.display.set_mode((screen_width, screen_height - 50), pygame.RESIZABLE)
                        self.editor.screen = pygame.display.get_surface()

                        # Set the full screen attributes to False
                        self.full_screen = False
                        self.editor.full_screen = False

                    # Changing from windowed to full screen
                    else:

                        # Set back to full screen mode
                        self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
                        self.editor.screen = pygame.display.get_surface()

                        # Set the full screen attributes to False
                        self.full_screen = True
                        self.editor.full_screen = True

                    # Re - adjust the static buttons (i.e. return and un-do button) according to the current screen height
                    self.undo_button.rect.y, self.return_to_editor_button.rect.y = self.screen.get_height() - self.undo_button_image.get_height() - 50, self.screen.get_height() - self.return_to_editor_button.image.get_height() - 50

                # -------------------------------------------------
                # Load menu events

                # If we are in the load menu
                if self.editor.show_load_menu == True and self.editor.show_editor == False:

                    # If the key that was pressed is a number and the tile map number selected is a double digit number
                    if event.unicode in string.digits and len(self.user_input_string) < 2:
                        # Concatenate the digit onto user_input_string
                        self.user_input_string += event.unicode

                    # If the user pressed the backspace key
                    if event.key == pygame.K_BACKSPACE and self.invalid_input == False:
                        # Remove the last item of the text and the user hasn't recently entered an invalid tile map
                        self.user_input_string = self.user_input_string[:-1]

                    # If the user pressed the return / enter key and the user input string is not empty and the user hasn't recently entered an invalid tile map
                    if event.key == pygame.K_RETURN and len(self.user_input_string) > 0 and self.invalid_input == False:

                        # If the tile map selected is a key in the existing tile maps dictionary
                        if int(self.user_input_string) in self.existing_tile_maps_dict.keys():

                            # Set the mouse cursor invisible again
                            pygame.mouse.set_visible(False)

                            # Output a message in the terminal to indicate that the tile map selected is being loaded
                            print(f"Loading tilemap {int(self.user_input_string)}...")

                            # Set the number of the editor's tile map selected to be the same as in the text file
                            self.editor.tile_map_selected_number = int(self.user_input_string)

                            # Load the existing tile map into the editor
                            self.load_existing_tile_map(tile_map = self.existing_tile_maps_dict[int(self.user_input_string)])

                            # Reset the attribute that states whether the load menu has been updated
                            self.load_tile_maps_menu_updated = False

                            # Reset the user input string so that the next time the user loads the menu, the text will be empty
                            self.user_input_string = ""

                            # Show the editor and stop showing the load menu
                            self.editor.show_editor = True
                            self.editor.show_load_menu = False

                        # If the tile map selected isn't a key in the existing tile maps dictionary
                        else:
                            # Set the invalid input variable to True
                            self.invalid_input = True

                            # Record the time that the user got the 
                            self.invalid_input_time = pygame.time.get_ticks()

                # -------------------------------------------------
                # Manage tile maps menu events

                # If we are in the manage tile maps menu          
                if self.editor.show_manage_tile_maps_menu == True and self.editor.show_editor == False:
                    
                    # If the user is pressing the "w" key and is not trying to move up when they are at the top of the menu
                    if event.key == pygame.K_w and self.menu_origin_point.y > 0:

                        # Move up the menu
                        self.menu_origin_point.y -= screen_height

                        # Decrement the current page we are on
                        self.current_page -= 1
                    
                        # Move the buttons down (so that we can the correct buttons are displayed on screen)
                        for button in self.manage_tile_maps_buttons_group:
                            button.rect.y += screen_height

                    # If the user is pressing the "s" key and the user is not on the last page
                    if event.key == pygame.K_s and self.current_page != self.num_of_pages:

                        # Move down the menu
                        self.menu_origin_point.y += screen_height

                        # Increment the current page we are on
                        self.current_page += 1

                        # Move the buttons up (so that we can the correct buttons are displayed on screen)
                        for button in self.manage_tile_maps_buttons_group:
                            button.rect.y -= screen_height

            # If the user has pressed the left mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # ----------------------------------------------------------------------------------------
                # If we are in the manage tile maps menu          
                if self.editor.show_manage_tile_maps_menu == True and self.editor.show_editor == False:

                    # For all tile map buttons in the manage tile maps menu
                    for button in self.manage_tile_maps_buttons_group:

                        # If it collides with the rectangle of the button
                        if self.mouse_rect.colliderect(button.rect):

                            # Check what the button's purpose is
                            match button.purpose:
                                
                                # Select button
                                case "Select":
                                    
                                    # If the user hasn't clicked on a select button before
                                    if self.first_selected_tile_map_for_swapping == None:
                                        # Select the tile map
                                        self.select_tile_map_for_swapping(button)

                                    # If the user pressed the deselect button
                                    elif self.first_selected_tile_map_for_swapping == button.stored_tile_map:
                                        # Deselect the tile map
                                        self.deselect_tile_map_for_swapping(button)
                                
                                # Swap button
                                case "Swap":
                                    
                                    # If the selected tile map for swapping is not the same as the tile map stored in the swap button and is not None
                                    if self.first_selected_tile_map_for_swapping != button.stored_tile_map and self.first_selected_tile_map_for_swapping != None:
                                        
                                        # Set action performed to True
                                        self.action_performed = True

                                        # Swap the tile maps
                                        self.swap_tile_maps(button)
                 
                                        # Record the time that the swap was made
                                        self.swap_made_time = pygame.time.get_ticks() 
                                    
                                    # ---------------------------------------------
                                    # Resetting the select button image

                                    # Iterate through the buttons group to find the button that was previously selected
                                    for previously_selected_button in self.manage_tile_maps_buttons_group:
                                        
                                        # If the button was the button that was previously selected 
                                        if previously_selected_button.purpose == "Select" and previously_selected_button.stored_tile_map == self.first_selected_tile_map_for_swapping:

                                            # Deselect the tile map
                                            self.deselect_tile_map_for_swapping(previously_selected_button)    

                                # Delete button
                                case "Delete":

                                    # Set action performed to True
                                    self.action_performed = True
                                    
                                    # Delete the tile map from the text file based on the line number in the text file
                                    self.delete_tile_map(tile_map_number = button.stored_tile_map_number)

                    # If the mouse rect collides with the rect of the undo button
                    if self.mouse_rect.colliderect(self.undo_button.rect):
                        # If the use had deleted / swapped tile maps previously
                        if self.action_performed == True:
                            # Undo the action (Works for undoing swaps and deletions)
                            self.undo_action()

                    # If the mouse rect collides with the rect of the return to editor button
                    if self.mouse_rect.colliderect(self.return_to_editor_button.rect):

                        # Set the mouse cursor invisible again
                        pygame.mouse.set_visible(False)

                        # Show the editor and stop showing the load menu
                        self.editor.show_editor = True
                        self.editor.show_manage_tile_maps_menu = False

                        # Reset the attribute that states whether the load menu has been updated
                        self.manage_tile_maps_menu_updated = False

                        # Reset the first selected tile map for swapping
                        self.first_selected_tile_map_for_swapping = None

                        # Reset the menu origin point's y co-ordinate, so that the user starts at the top of the menu again
                        self.menu_origin_point.y = 0

    def run(self):

        # Run the event loop
        self.event_loop()
        
        # ----------------------------------------------------------------------------------------
        # Program states

        # If we need to show the editor
        if self.editor.show_editor == True:

            # Run the editor
            self.editor.run()

        # If we don't need to show the editor
        else:
            
            # ----------------------------------------------------------------------------------------
            # All menus

            # Execute common functionality across all menus
            self.execute_common_menu_functionality()
       
            # ----------------------------------------------------------------------------------------
             # Specific to each menus

            # If we need to show the load menu
            if self.editor.show_load_menu == True:  

                # If the load menu hasn't been updated yet
                if self.load_tile_maps_menu_updated == False:

                    # Update the load tile maps menu with all the necessary information once
                    self.update_menus()
                    
                    # The load tile maps menu is now updated
                    self.load_tile_maps_menu_updated = True

                # Show the load tile maps menu
                self.loading_tile_map_input()    

            elif self.editor.show_manage_tile_maps_menu == True:

                # If the manage tile maps menu hasn't been updated yet
                if self.manage_tile_maps_menu_updated == False:

                    # Update the manage tile maps menu with all the necessary information once
                    self.update_menus()

                    # Create the buttons for this menu (This must be done each time the menu is loaded as the user may have created a new tile map)
                    self.create_buttons()

                    # Calculate the number of pages there are according to how many tile maps there are
                    self.calculate_pages()

                    # Create an attribute which is used to track which page the user is on
                    self.current_page = 1

                    # The manage tile maps menu is now updated
                    self.manage_tile_maps_menu_updated = True

                # Show the manage tile maps menu
                self.manage_tile_maps_menu()

        # ----------------------------------------------------------------------------------------
        # Automatically saving

        # If we need to automatically save progress (This only occurs when the user has made changes to the tile map in the editor)
        if self.editor.automatically_save_progress == True:
            
            # Save the progress onto the tile maps text file
            self.automatically_save_progress()
