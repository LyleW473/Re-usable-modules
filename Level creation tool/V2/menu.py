import pygame, sys, string
from settings import *
from button import Button
from extra_functions import *
from pygame import image as pyi

class Menu:

    def __init__(self, tile_size, origin_point, tile_list):
        
        # Set the display as the current display
        self.screen = pygame.display.get_surface()
        self.full_screen = False

        # Set the tile size to be the same as the tile size declared on the DrawingTiles class
        self.tile_size = tile_size

        # The origin point should be (0, 0) upon instantiation
        self.origin_point = origin_point

        # The tile list should be an empty tile map upon instantiation
        self.tile_list = tile_list

        # Holds all the existing tile maps
        self.existing_tile_maps_dict = {}

    # ----------------------------------------------------------------------------------------
    # Helper methods

    def mouse_position_updating(self):
        # Used to update the mouse position and mouse rect
        
        # Retrieve the mouse position
        self.mouse_position = pygame.mouse.get_pos()

        # Define the mouse rect and draw it onto the screen (For collisions with drawing tiles)
        self.mouse_rect = pygame.Rect(((-self.origin_point.x) + self.mouse_position[0], self.mouse_position[1], 20, 20))

    def find_existing_tile_maps(self):
        # Finds out the number of tile maps in the text file and updates the existing tile maps dictionary with the contents

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

    # ----------------------------------------------------------------------------------------
    # Loading methods

    def loading_tile_map_input(self, origin_point): 

        # Set / update the origin point as an attribute (so that the rectangles are positioned properly in the case that the user moved the camera right)
        self.origin_point = origin_point

        # Set the mouse cursor as visible when asking for user input when loading a tile map
        pygame.mouse.set_visible(True)

        # ------------------------------------------------
        # Find out the number of tile maps and save it to the dictionary
        
        self.find_existing_tile_maps()

        # ------------------------------------------------
        # Handling user input for choosing tile map

        # Define an empty user input string, font used, the user input box and a variable which tracks whether the user entered an invalid tile map
        user_input_string = ""
        user_input_font = pygame.font.SysFont("Bahnschrift", 40)
        user_input_rectangle = pygame.Rect((screen_width / 2) - 110, (screen_height / 2) - 30, 200, 60)
        invalid_input = False

        # Create a button to go back to the editor
        return_to_editor_button = Button((screen_width / 2) - 250 + abs(self.origin_point.x), user_input_rectangle.y + 250, pyi.load("V2/graphics/buttons/user_input/return_to_editor_button.png"))

        # If the full screen attribute is True
        if self.full_screen == True:
            
            # Set the screen to full screen
            self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
        
        # Continuously ask for user input 
        while True: 
            # ------------------------------------------------
            # Menu display

            # Fill the screen with grey
            self.screen.fill("gray17") 

            # Display the instructions onto the screen
            draw_text("Please enter a tile map", user_input_font, "white", user_input_rectangle.x - 100, user_input_rectangle.y - 60, self.screen)

            # Display the user input string onto the screen
            draw_text(user_input_string, user_input_font, "white", user_input_rectangle.x + 10, user_input_rectangle.y + 10, self.screen)

            # Display the number of tile maps text onto the screen
            draw_text(f"There are {len(self.existing_tile_maps_dict)} tile maps.", user_input_font, "dodgerblue4", user_input_rectangle.x - 90, user_input_rectangle.y - 160, self.screen)

            # Draw a rectangle for the user input 
            pygame.draw.rect(self.screen, "black", user_input_rectangle, 5)

            # Draw the return to editor button
            return_to_editor_button.draw((screen_width / 2) - 250, user_input_rectangle.y + 250)

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
            # Handle mouse input

            # Update the mouse position and mouse rect
            self.mouse_position_updating()

            # If the user has pressed the left click
            if pygame.mouse.get_pressed()[0]:

                # If the mouse rect collides with the rect of the save as new tile map button
                if self.mouse_rect.colliderect(return_to_editor_button.rect):

                    # Set the mouse cursor invisible again
                    pygame.mouse.set_visible(False)

                    # Return None (this will mean that nothing happens inside the save_tile_map method)
                    return None
            
            # ------------------------------------------------
            # Event handler
            for event in pygame.event.get():
                
                # If the user pressed a key
                if event.type == pygame.KEYDOWN:

                    # If the key that was pressed is a number and the tile map number selected is a double digit number
                    if event.unicode in string.digits and len(user_input_string) < 2:
                        # Concatenate the digit onto user_input_string
                        user_input_string += event.unicode

                    # If the user pressed the backspace key
                    if event.key == pygame.K_BACKSPACE and invalid_input == False:
                        # Remove the last item of the text and the user hasn't recently entered an invalid tile map
                        user_input_string = user_input_string[:-1]

                    # If the user pressed the return / enter key and the user input string is not empty and the user hasn't recently entered an invalid tile map
                    if event.key == pygame.K_RETURN and len(user_input_string) > 0 and invalid_input == False:

                        # If the tile map selected is a key in the existing tile maps dictionary
                        if int(user_input_string) in self.existing_tile_maps_dict.keys():

                            # Set the mouse cursor invisible again
                            pygame.mouse.set_visible(False)

                            # Output a message in the terminal to indicate that the tile map selected is being loaded
                            print(f"Loading tilemap {int(user_input_string)}...")
                            
                            # Set the existing tile map selected as the tilemap and the user input string
                            self.existing_tile_map_selected = [ self.existing_tile_maps_dict[int(user_input_string)], int(user_input_string) ]

                            # Return a list containing: the tile map (this is fed into the load_existing_tile_map method) and which tile map number it is
                            return [ self.existing_tile_maps_dict[int(user_input_string)], int(user_input_string) ]


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

        # If tile map is None, it means the user pressed the "Return to editor button"
        if tile_map == None:
            # Exit the method
            return None

        # Set the string_tile_list as the tile map selected by the user from the loading_tile_map_input method
        string_tile_list = tile_map[0]

        # Reset self.tile_list so that if the user tried loading multiple tilemaps, only one tile map is displayed at a time
        self.tile_list = []

        # Save the tile map selected and the number the tile map is as an at tribute
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

        # Return the tile map and the selected tile map's number to the drawing canvas / main program
        return [self.tile_list, self.existing_tile_map_selected[1]]
    
    # ----------------------------------------------------------------------------------------
    # Saving methods

    def save_tile_map(self, automatically_save_variable = None):

        # ----------------------------------------------------------------------------------------
        # Automatic saving

        # If the automatically save variable has been set to True and the user has selected an existing tile map
        if automatically_save_variable == True and hasattr(self, "existing_tile_map_selected") == True:
            # Save the progress onto the current tile map selected
            save_as_new_tile_map = False

            print("Progress has been saved.")

        # If the automatically save variable has been set to True but the user hasn't selected an existing tile map
        elif automatically_save_variable == True and hasattr(self, "existing_tile_map_selected") == False:

            # Save the progress as a new tile map
            save_as_new_tile_map = True

        # ----------------------------------------------------------------------------------------
        # Convert the current tile map into a tile map of its palette numbers

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

        # ----------------------------------------------------------------------------------------
        # Save the tile map according to the user's choice

        # If the user has chosen to overwrite the existing tile map selected
        if save_as_new_tile_map == False:

                # Open the file to read the contents
                with open("V2/existing_tile_maps.txt", "r") as existing_tile_maps_file:
                    # Read the contents of the file and save it to a variable
                    existing_tile_maps_file_content = existing_tile_maps_file.read()

                    # Replace the old tile map stored in the text with the tile map to be saved
                    existing_tile_maps_file_content = existing_tile_maps_file_content.replace(self.existing_tile_map_selected[0], str(tile_map_to_be_saved))

                    # Set the existing tile map selected as the saved tile map
                    self.existing_tile_map_selected[0] = str(tile_map_to_be_saved)

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

        # If the status is "Unsuccessful"
        if status == "Unsuccessful":

            # Return "Unsuccessful" to the drawing canvas / main program
            return "Unsuccessful"

    # def manage_tile_maps(self, origin_point):

    #     # Set / update the origin point as an attribute (so that the rectangles are positioned properly in the case that the user moved the camera right)
    #     self.origin_point = origin_point

    #     # Set the mouse cursor as visible when asking for user input when loading a tile map
    #     pygame.mouse.set_visible(True)

    #     # Create the buttons for this menu
    #     # Note: The buttons are (500 x 125) pixels
    #     # Define positioning (Easy to modify)
    #     button_x_position = (screen_width / 2) - 250
    #     button_y_position = 250

    #     save_as_new_tile_map_button = Button(button_x_position + abs(self.origin_point.x), button_y_position, pyi.load("V2/graphics/buttons/user_input/save_as_new_tile_map_button.png"))
    #     overwrite_selected_tile_map_button = Button(button_x_position + abs(self.origin_point.x), button_y_position + 150, pyi.load("V2/graphics/buttons/user_input/overwrite_selected_tile_map_button.png"))
    #     return_to_editor_button = Button(button_x_position + abs(self.origin_point.x), button_y_position + 300, pyi.load("V2/graphics/buttons/user_input/return_to_editor_button.png"))
        
    #     # Define a font 
    #     existing_tile_map_selected_font = pygame.font.SysFont("Bahnschrift", 40)

    #     # Continuously ask for user input 
    #     while True:         
            
    #         # ----------------------------------------------------------------------------------------
    #         # Display:

    #         # Fill the screen with grey
    #         self.screen.fill("gray17") 

    #         # Draw the buttons on screen
    #         save_as_new_tile_map_button.draw(button_x_position, button_y_position)
    #         overwrite_selected_tile_map_button.draw(button_x_position, button_y_position + 150)
    #         return_to_editor_button.draw(button_x_position, button_y_position + 300)

    #         # If a tile map has been selected
    #         if hasattr(self, "existing_tile_map_selected"):
    #             # Draw a text indicating the number of the tile map selected
    #             draw_text(f"Selected tile map: {self.existing_tile_map_selected[1]}", existing_tile_map_selected_font, "white", button_x_position + 40 , button_y_position - 80, self.screen)
    #         # Otherwise
    #         else:
    #             # Draw a text indicating that there is no tile map selected
    #             draw_text("Selected tile map: None", existing_tile_map_selected_font, "white", button_x_position + 40 , button_y_position - 80, self.screen)

    #         # ----------------------------------------------------------------------------------------
    #         # Handle mouse input

    #         # Update the mouse position and mouse rect
    #         self.mouse_position_updating()

    #         # If the user has pressed the left click
    #         if pygame.mouse.get_pressed()[0]:

    #             # If the mouse rect collides with the rect of the save as new tile map button
    #             if self.mouse_rect.colliderect(save_as_new_tile_map_button.rect):

    #                 # Set the mouse cursor invisible again
    #                 pygame.mouse.set_visible(False)

    #                 # Return True, meaning that the user wants to save the current tile map as a new tile map
    #                 return True

    #             # If the mouse rect collides with the rect of the overwrite selected tile map button
    #             elif self.mouse_rect.colliderect(overwrite_selected_tile_map_button.rect):
                    
    #                 # If there is an attribute called self.existing_tile_map_selected, it means the user has chosen a tile map to overwrite
    #                 if hasattr(self, "existing_tile_map_selected"):

    #                     # Set the mouse cursor invisible again
    #                     pygame.mouse.set_visible(False)

    #                     # Return False, meaning that the user wants to save it onto the existing tile map selected / loaded
    #                     return False

    #                 # Otherwise:
    #                 else:
    #                     print("You have not selected a tile map to overwrite")
                
    #             # If the mouse rect collides with the rect of the return to editor button
    #             elif self.mouse_rect.colliderect(return_to_editor_button.rect):

    #                 # Set the mouse cursor invisible again
    #                 pygame.mouse.set_visible(False)

    #                 # Return None (this will mean that nothing happens inside the save_tile_map method)
    #                 return None


    #         # Event handler
    #         for event in pygame.event.get():

    #             # If the exit button was pressed
    #             if event.type == pygame.QUIT:
    #                 # Close the program
    #                 pygame.quit()
    #                 sys.exit()

    #         # Update the display
    #         pygame.display.update()