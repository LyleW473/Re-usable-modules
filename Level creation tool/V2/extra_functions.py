def draw_text(text, font, text_colour, x, y , surface):
    # Render the text as an image onto the surface
    image = font.render(text, True, text_colour)
    
    # Draw the image text onto the surface
    surface.blit(image, (x, y))

def draw_alpha_text(text, font, text_colour,  x, y, surface):
    # Render the text as an image onto the surface
    alpha_text = font.render(text, True ,text_colour)

    # Set the alpha level of the text 
    alpha_text.set_alpha(70)

    # Draw the image text onto the surface
    surface.blit(alpha_text,(x,y))