import pygame, sys
from settings import *
from drawing_canvas import DrawingTiles



class Main:

    def __init__(self):

        # Pygame set-up
        pygame.init()

        # Set the caption
        pygame.display.set_caption("Level creator")

        # Set the display as full screen
        self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)

        # Limit fps
        self.clock = pygame.time.Clock()  

        # Create a drawing canvas  
        self.drawing_canvas = DrawingTiles()


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
            # MAIN PROGRAM
            self.screen.fill("gray17") 

            # Run all of the drawing canvas methods
            self.drawing_canvas.run()

            # -------------------------------------
            # Update display
            pygame.display.update() 

            # Limit FPS to 60
            self.clock.tick(60)


    
if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()