# python
import pygame as pg
import physics as ph

screen = None
font = None

def start_graphics(width=800, height=600):
    global screen, font
    pg.init()
    pg.display.set_caption("Gravity Simulation")
    # create a resizable window (not fullscreen)
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)
    font = pg.font.SysFont(None, 24)

def resize(width, height):
    global screen
    # recreate the window at the new size while keeping it resizable
    screen = pg.display.set_mode((width, height), pg.RESIZABLE)

def world_to_screen(wx, wy, cam, zoom):
    """Convert world coordinates to screen coordinates."""
    sw, sh = screen.get_size()
    cx, cy = cam
    sx = (wx - cx) * zoom + sw / 2
    sy = (wy - cy) * zoom + sh / 2
    return int(sx), int(sy)

def draw_objects(objects, mult=None, creating=None, cam=(0,0), zoom=1):
    global screen, font
    screen.fill((0, 0, 0))  # Clear screen with black

    sw, sh = screen.get_size()

    # draw objects with larger ones first so smaller objects appear on top
    for obj in sorted(objects, key=lambda o: o.size, reverse=True):
        sx, sy = world_to_screen(obj.x, obj.y, cam, zoom)
        r = max(1, int(obj.size * zoom))
        pg.draw.circle(screen, obj.color, (sx, sy), r)

    # draw creation preview (translucent circle and velocity vector)
    if creating:
        # creating is expected to be a dict with keys: stage, x, y, rad, mouse_pos
        stage = creating.get('stage', 0)
        cx_world = creating.get('x', 0)
        cy_world = creating.get('y', 0)
        rad_world = creating.get('rad', 0)
        mouse_pos = creating.get('mouse_pos', (0,0))

        # convert creation center to screen coords
        cx, cy = world_to_screen(cx_world, cy_world, cam, zoom)

        # clamp radius so preview surface stays reasonable within current window
        rad_screen = max(1, int(rad_world * zoom))
        max_rad = min(sw, sh) // 2
        rad_int = max(1, int(min(rad_screen, max_rad)))

        # translucent surface for preview circle
        if stage >= 1 and rad_world > 0:
            preview_surf = pg.Surface((rad_int*2+4, rad_int*2+4), pg.SRCALPHA)
            preview_color = (200, 200, 255, 80)  # translucent bluish
            pg.draw.circle(preview_surf, preview_color, (rad_int+2, rad_int+2), rad_int)
            screen.blit(preview_surf, (cx - rad_int - 2, cy - rad_int - 2))

            # outline
            pg.draw.circle(screen, (200,200,255), (cx, cy), rad_int, 1)

        # velocity vector preview (arrow)
        if stage == 2:
            mx, my = mouse_pos  # mouse pos is screen coords
            # draw line from creation center (screen) to mouse
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
            instruct = "Left-click to set radius (move mouse to preview)"
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