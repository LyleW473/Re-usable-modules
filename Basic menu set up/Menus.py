# Import modules
import pygame, sys

# Initialise pygame
pygame.init()

# Screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Load images 
# Most buttons are (400 x 25) pixels
play_image = pygame.image.load('graphics/Buttons/play_button.png').convert()
controls_image = pygame.image.load('graphics/Buttons/controls_button.png').convert()
quit_image = pygame.image.load('graphics/Buttons/quit_button.png').convert()
back_image = pygame.image.load('graphics/Buttons/back_button.png').convert()
return_to_main_menu_image = pygame.image.load('graphics/Buttons/return_to_main_menu_button.png').convert()
continue_image = pygame.image.load('graphics/Buttons/continue_button.png').convert()


# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, pos):
        mouse_over_button = False
        # Check for a collision between the button and the current mouse position
        if self.rect.collidepoint(pos):
            mouse_over_button = True

        # Draw the button
        screen.blit(self.image, self.rect)

        # Return the clicked variable to the menu
        return mouse_over_button



class Menu():
    def __init__(self, x, y, surface):
        # Surface that the menu will be drawn onto
        self.surface = surface
        # Buttons
        self.button_list = []
        self.clicked = False # Used to track whenever the buttons on the menus are clicked

        # Game states
        self.show_main_menu = True # Determines whether we show the main menu or not
        self.show_controls_menu = False
        self.in_game = False # Determines whether we are in game or not
        self.show_paused_menu = False

        self.last_menu_visited = 0 # 1 = Main menu, 2 = Paused menu


    def update(self, pos):

        # MAIN MENU
        if self.show_main_menu == True:
            # Fill the screen with a white background
            screen.fill(WHITE)

            # PLAY BUTTON
            # If the mouse is over the play button and is the mouse button is clicked
            if play_button.update(pos) == True and self.clicked == True: 
                print("play button clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False
                # Set the main menu to stop showing and start the game
                self.show_main_menu = False
                self.in_game = True

            # CONTROLS BUTTON
            if controls_button.update(pos) == True and self.clicked == True: 
                print("controls button clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Display the show controls menu
                self.show_controls_menu = True
                self.show_main_menu = False

                # Set the last menu visited from the controls menu to be the paused menu
                self.last_menu_visited = 1

            # QUIT BUTTON
            # If the mouse is over the quit button and is the mouse button is clicked
            if quit_button.update(pos) == True and self.clicked == True:
                print("quit button clicked")
                # Quit the game
                pygame.quit()
                sys.exit()

            # If none of the buttons above are True, that means the player clicked on empty space
            elif play_button.update(pos) == False and quit_button.update(pos) == False and self.clicked == True: 
                print("empty space clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

            
        # CONTROLS MENU
        if self.show_controls_menu == True:
            screen.fill(GREEN)

            # BACK BUTTON
            if back_button.update(pos) == True and self.clicked == True:
                print("back button clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Go back to the last menu 
                if self.last_menu_visited == 1: # MAIN MENU
                    self.show_main_menu = True

                elif self.last_menu_visited == 2: # PAUSED MENU
                    self.show_paused_menu = True

                # Don't show the controls menu
                self.show_controls_menu = False

            # If none of the buttons above are True, that means the player clicked on empty space
            elif back_button.update(pos) == False and self.clicked == True: 
                print("empty space clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False


        # PAUSED MENU
        if self.show_paused_menu == True:
            screen.fill(RED)
            
            # CONTINUE BUTTON
            if continue_button.update(pos) == True and self.clicked == True: 
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Go back to the main game
                self.in_game = True
                self.show_paused_menu = False

            # CONTROLS BUTTON
            if controls_button_2.update(pos) == True and self.clicked == True: 
                print("controls button clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False

                # Display the show controls menu
                self.show_controls_menu = True
                self.show_paused_menu = False   
                
                # Set the last menu visited from the controls menu to be the paused menu
                self.last_menu_visited = 2

            # QUIT BUTTON
            # If the mouse is over the quit button and is the mouse button is clicked
            if quit_button_2.update(pos) == True and self.clicked == True:
                print("quit button clicked")
                # Quit the game
                pygame.quit()
                sys.exit()

            # If none of the buttons above are True, that means the player clicked on empty space
            elif continue_button.update(pos) == False and controls_button_2.update(pos) == False and quit_button_2.update(pos) == False:
                print("empty space clicked")
                # Reset the clicked variable to default so more clicks can be detected
                self.clicked = False             
      



# Button instances

# Main menu
play_button = Button(300, 200 , play_image)
controls_button = Button(300, 400, controls_image)
quit_button = Button(300, 600, quit_image)

# Controls menu
back_button = Button(300, 600, back_image)
return_to_main_menu_button = Button(300, 400, return_to_main_menu_image)


# Paused menu
continue_button = Button(300, 200, continue_image)
controls_button_2 = Button(300, 400, controls_image)
quit_button_2 = Button(300, 600, quit_image)