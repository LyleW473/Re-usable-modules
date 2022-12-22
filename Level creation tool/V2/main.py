import pygame, sys
from settings import *


class Main:

    def __init__(self):

        # Pygame set-up
        pygame.init()
        pygame.display.set_caption("Level creator")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

    def run(self):

        while True:
            
            # Event handler
            for event in pygame.event.get():

                # If the exit button was pressed
                if event.type == pygame.QUIT:
                    # Close the program
                    pygame.quit()
                    sys.exit()
                
            # -------------------------------------
            # Update display
            pygame.display.update() 
            # Limit FPS to 60
            self.clock.tick(60)


    
if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()