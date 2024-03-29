import pygame
from settings import *
from menu import Menu



class Main:

    def __init__(self):

        # Pygame set-up
        pygame.init()

        # Set the caption
        pygame.display.set_caption("Level creator")

        # Set the display as full screen
        self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)

        # Create an object to track time
        self.clock = pygame.time.Clock()  

        # Create a menu
        self.menu = Menu()


    def run(self):

        while True:
            # -------------------------------------
            # MAIN PROGRAM

            # Start running the menu
            self.menu.run()

            # -------------------------------------
            # Update display
            pygame.display.update() 

            # Limit FPS to 60
            self.clock.tick(60)

    
if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()