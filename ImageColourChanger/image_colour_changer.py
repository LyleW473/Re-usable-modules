import pygame
from time import perf_counter
from sys import exit as system_exit


class Main:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("WindowedAndFullscreenSwitching")
        
        # Define the screen width and height (this will be the size of the window in windowed mode)
        # Resolutions with aspect ratios that are not 16:9 will result in black bars
        self.screen_width = 1600
        self.screen_height = 900

        """ Set the screen to be full screen and scale the 1600 x 900 resolution to 1920 x 1080 (or the maximum size of the user's monitor)
        - SCALED scales the 1600 x 900 up to the native resolution of the user.
        - FULLSCREEN sets the program to full screen
        """
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED + pygame.FULLSCREEN)

        # Define a scale multiplier (everything will be scaled up by this amount)
        self.scale_multiplier = 8
        
        # Create a scaled surface based on the scale multiplier
        self.scaled_surface = pygame.Surface((self.screen_width / self.scale_multiplier, self.screen_height/ self.scale_multiplier))

        # Attribute to track if the user is in full-screen or windowed mode
        self.full_screen = True 

        # Sample image
        self.sample_image = pygame.image.load("sample_image.png").convert_alpha()

        # --------------------------------------------
        # Time
        
        # Record the previous frame that was played
        self.previous_frame = perf_counter()
        
        # Create an object to track time
        self.clock = pygame.time.Clock()
        self.chosen_framerate = 60

    def event_loop(self):

        for event in pygame.event.get():
            
            # If the user has pressed the exit button
            if event.type == pygame.QUIT:
                # Exit the program
                pygame.quit()
                system_exit()
            
            # If the user has pressed a key
            if event.type == pygame.KEYDOWN:
                
                # If the "f" key is pressed
                if event.key == pygame.K_f:

                    # If the user is currently in full-screen mode
                    if self.full_screen == True:
                        # Set the screen to be in windowed mode
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                        # Set the full screen attribute to False
                        self.full_screen = False
                    
                    # If the user is currently in windowed mode
                    elif self.full_screen == False:
                        # Set the screen to be in full-screen mode
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED + pygame.FULLSCREEN)
                        # Set the full screen attribute to True
                        self.full_screen = True        
    
    def change_image_colour_v1(self):
        
        # Create a copy of the current image
        changed_image = self.sample_image.copy()

        # For each row
        for i in range(0, self.sample_image.get_width()):
            # For each column
            for j in range(0, self.sample_image.get_height()):
                
                # If the pixel is not black
                if self.sample_image.get_at((i, j)) != (0, 0, 0, 255):
                    # Set the pixel as white
                    changed_image.set_at((i, j), (255, 255, 255, 255))

        # Return the changed image
        return changed_image
    
    def change_image_colour_v2(self, current_animation_image, desired_colour = (255, 255, 255)): # Default colour is white (CAN BE CHANGED INTO FUNCTION BY REMOVING SELF)

            # Create a new surface which will be blended with the current (animation) image to make an image change colour
            colour_layer = pygame.Surface(current_animation_image.get_size()).convert_alpha() 

            # Fill the colour layer with the desired colour
            colour_layer.fill(desired_colour)
            
            # Set the current (animation) image to be a copy of the current (animation) image (so that the original image is not overwritten)
            current_animation_image = current_animation_image.copy()
            
            # Blit the colour layer onto the current (animation) image, with the special flag pygame_BLEND_RGB_ADD (can use other flags, e.g. MULT, MAX, etc.) to add the RGB values
            current_animation_image.blit(colour_layer, (0, 0), special_flags = pygame.BLEND_RGB_ADD)

            # Return the coloured animation image (The result should be an image that has a different colour on top)
            return current_animation_image

    def run(self):
 
        while True:
 
            
            # Limit FPS to 60
            self.clock.tick(self.chosen_framerate)

            # Calculate delta time 
            delta_time = perf_counter() - self.previous_frame
            self.previous_frame = perf_counter()

            # Run the event loop
            self.event_loop()

            # Find the colour at a 
            colour = self.sample_image.get_at((int(self.sample_image.get_width() / 2), int(self.sample_image.get_height() / 2)))

            # Fill the scaled surface with blue
            self.scaled_surface.fill("blue")

            # If the spacebar is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                
                changed_image = self.change_image_colour_v2(current_animation_image = self.sample_image, desired_colour = "green")
                # Draw the image with a changed colour
                self.scaled_surface.blit(changed_image, ((self.scaled_surface.get_width() / 2) - (changed_image.get_width() / 2), (self.scaled_surface.get_height() / 2) - (changed_image.get_height() / 2)))
            # Otherwise
            else:
                # Blit the sample image onto the screen
                self.scaled_surface.blit(self.sample_image, ((self.scaled_surface.get_width() / 2) - (self.sample_image.get_width() / 2), (self.scaled_surface.get_height() / 2) - (self.sample_image.get_height() / 2)))

            # Blit the scaled surface onto the main screen
            self.screen.blit(pygame.transform.scale(self.scaled_surface, (self.screen_width, self.screen_height)), (0, 0))


            # -------------------------------------
            # Update display
            pygame.display.update() 
            

if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()