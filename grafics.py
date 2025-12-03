# python
import pygame as pg
import physics as ph

screen = None
font = None

def start_graphics():
    global screen, font
    pg.init()
    pg.display.set_caption("Gravity Simulation")
    # Open a fullscreen window
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    font = pg.font.SysFont(None, 24)

def draw_objects(objects, mult=None):
    global screen, font
    screen.fill((0, 0, 0))  # Clear screen with black

    for obj in objects:
        pg.draw.circle(screen, obj.color, (int(obj.x), int(obj.y)), int(obj.size))

    # draw time multiplier once per frame
    if font is None:
        font = pg.font.SysFont(None, 24)
    text_surface = font.render(f'Time multiplier: {mult}', True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pg.display.flip()

def stop_graphics():
    pg.quit()