# Import modules
import pygame, sys
from pygame.locals import *


# Initialise pygame
pygame.init()

# Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (93,93,93)

# Fonts
user_input_font = pygame.font.SysFont("Bahnschrift", 40)

def draw_text(text, font, text_colour, x, y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (x, y))

user_text = "" # Holds the numbers that the user types into the input box 
user_input_rectangle = pygame.Rect((screen_width / 2) - 100, screen_height - 90, 200, 50) # User input box rectangle

# Main loop
pygame.key.set_repeat(1, 100)
run = True
while run:

    text_image = user_input_font.render(user_text, True, BLACK)
    pygame.draw.rect(screen, WHITE, user_input_rectangle, 0)
    pygame.draw.rect(screen, BLACK, user_input_rectangle, 5)
    screen.blit(text_image, (user_input_rectangle.x + 10, user_input_rectangle.y + 8))
    user_input_rectangle.width = max(200, text_image.get_width() + 20)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            print(event.key)


    pygame.display.update()
