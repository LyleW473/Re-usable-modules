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
        self.screen = pygame.display.set_mode((screen_width, screen_height - 50), pygame.RESIZABLE) # -50 because of the title bar at the top of the screen
        self.full_screen = False

        # Limit fps
        self.clock = pygame.time.Clock()  

        # Create a drawing canvas  
        self.drawing_canvas = DrawingTiles()


    def run(self):

        while True:
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

            # Event handler
            for event in pygame.event.get():

                # If the user pressed a key
                if event.type == pygame.KEYDOWN:
                    
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
                            self.drawing_canvas.screen = pygame.display.get_surface()
                            self.drawing_canvas.menu.screen = pygame.display.get_surface()

                            # Set the full screen attributes to False
                            self.full_screen = False
                            self.drawing_canvas.full_screen = False
                            self.drawing_canvas.menu.full_screen = False


                        # Changing from windowed to full screen
                        else:

                            # Set back to full screen mode
                            self.screen = pygame.display.set_mode(flags = pygame.FULLSCREEN)
                            self.drawing_canvas.screen = pygame.display.get_surface()
                            self.drawing_canvas.menu.screen = pygame.display.get_surface()

                            # Set the full screen attributes to True
                            self.full_screen = True
                            self.drawing_canvas.full_screen = True
                            self.drawing_canvas.menu.full_screen = True


                # If the exit button was pressed
                if event.type == pygame.QUIT:
                    # Close the program
                    pygame.quit()
                    sys.exit()

    
if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()