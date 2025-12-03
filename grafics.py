import pygame as pg
import physics as ph


# start graphics function
def start_graphics():
    global screen
    pg.init()
    pg.display.set_caption("Gravity Simulation")
    screen = pg.display.set_mode((800, 600))


# draw objects function
def draw_objects(objects, mult=None):
    # same display
    global screen
    screen.fill((0, 0, 0))  # Clear screen with black
    for obj in objects:
        # Draw each object as a circle with random color
        pg.draw.circle(screen, obj.color, (int(obj.x), int(obj.y)), int(obj.size))

        # draw time multiplier
        font = pg.font.SysFont(None, 24)
        text_surface = font.render(f'Time multiplier: {mult}', True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))  # Position the text at (10, 10)
        # Update the display
    pg.display.flip()


# quit graphics function


pg.quit()
