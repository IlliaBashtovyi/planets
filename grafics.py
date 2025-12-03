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

def draw_objects(objects, mult=None, creating=None):
    global screen, font
    screen.fill((0, 0, 0))  # Clear screen with black

    # draw objects with larger ones first so smaller objects appear on top
    for obj in sorted(objects, key=lambda o: o.size, reverse=True):
        pg.draw.circle(screen, obj.color, (int(obj.x), int(obj.y)), int(obj.size))

    # draw creation preview (translucent circle and velocity vector)
    if creating:
        # creating is expected to be a dict with keys: stage, x, y, rad, mouse_pos
        stage = creating.get('stage', 0)
        cx = int(creating.get('x', 0))
        cy = int(creating.get('y', 0))
        rad = creating.get('rad', 0)
        mouse_pos = creating.get('mouse_pos', (0,0))

        # translucent surface for preview circle
        if stage >= 1 and rad > 0:
            preview_surf = pg.Surface((rad*2+4, rad*2+4), pg.SRCALPHA)
            preview_color = (200, 200, 255, 80)  # translucent bluish
            pg.draw.circle(preview_surf, preview_color, (int(rad)+2, int(rad)+2), int(rad))
            screen.blit(preview_surf, (cx - rad - 2, cy - rad - 2))

            # outline
            pg.draw.circle(screen, (200,200,255), (cx, cy), int(rad), 1)

        # velocity vector preview (arrow)
        if stage == 2:
            mx, my = mouse_pos
            # draw line from creation center to mouse
            pg.draw.line(screen, (255,255,255), (cx, cy), (mx, my), 2)
            # simple arrowhead
            dx = mx - cx
            dy = my - cy
            length = max(1, (dx*dx + dy*dy) ** 0.5)
            ux, uy = dx/length, dy/length
            # two small lines for arrowhead
            left = (mx - int(10*(ux - uy)), my - int(10*(uy + ux)))
            right = (mx - int(10*(ux + uy)), my - int(10*(uy - ux)))
            pg.draw.line(screen, (255,255,255), (mx, my), left, 2)
            pg.draw.line(screen, (255,255,255), (mx, my), right, 2)

        # small instruction text
        if font is None:
            font = pg.font.SysFont(None, 24)
        if stage == 0:
            instruct = "Left-click to set position"
        elif stage == 1:
            instruct = "Right-click to set radius (move mouse to preview)"
        elif stage == 2:
            instruct = "Left-click to set velocity (drag) and create object"
        else:
            instruct = ""
        if instruct:
            txt = font.render(instruct, True, (200,200,200))
            screen.blit(txt, (10, 40))

    # draw time multiplier once per frame
    if font is None:
        font = pg.font.SysFont(None, 24)
    text_surface = font.render(f'Time multiplier: {mult}', True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pg.display.flip()

def stop_graphics():
    pg.quit()