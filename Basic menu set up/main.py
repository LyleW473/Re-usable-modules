# Import modules
import pygame, sys
from pygame.locals import *
from Menus import Menu


# Initialise pygame
pygame.init()

# Screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Game variables

# Instances
menu = Menu(0,0,screen)


# Main loop
run = True
while run:

    # Menu browsing and updating

    # Find the position of the mouse
    pos = pygame.mouse.get_pos()
    # Update the menu, feeding the clicked variable and mouse position into the function
    menu.update(pos) # Set the clicked variable as the returned value from the menu
    
    # INGAME
    if menu.in_game == True:
        screen.fill(BLUE)

    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()

        # Check if the mouse button has been pressed
        if event.type == MOUSEBUTTONDOWN:
            # Check if the mouse button clicked was the left click
            if event.button == 1: # (1 = left, 2 = middle, 3 = right, 4 = scroll up, 5 = scrolldown)
                menu.clicked = True

        # Check if a key has been pressed
        if event.type == KEYDOWN:
            # Check if we are in game
            if menu.in_game == True:    
                # If the ESC key is pressed
                if event.key == K_ESCAPE:
                    # Show the main menu
                    menu.show_main_menu = True
                    menu.in_game = False


    pygame.display.update()
