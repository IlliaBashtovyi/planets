import pygame as pg
import physics as f
import random as r


pg.init()
pg.display.set_caption("Gravity Simulation")
screen = pg.display.set_mode((800, 600))
time = 10


# draw objects function
def draw_objects(objects):
    # same display
    global screen
    screen.fill((0, 0, 0))  # Clear screen with black
    for obj in objects:
        # Draw each object as a circle with random color
        color = (r.randrange(0, 255), r.randrange(0, 255), r.randrange(0, 255))
        pg.draw.circle(screen, color, (int(obj.x), int(obj.y)), int(obj.size))
    pg.display.flip()


# draw arrow function
def arow(start_pos, end_pos, color=(255, 255, 255), arrow_size=10):
    # same display
    global screen
    pg.draw.line(screen, color, start_pos, end_pos, 2)
    direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    length = f.dist_points(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    if length == 0:
        return
    unit_dir = (direction[0] / length, direction[1] / length)
    left_wing = (end_pos[0] - unit_dir[0] * arrow_size - unit_dir[1] * (arrow_size / 2),
                 end_pos[1] - unit_dir[1] * arrow_size + unit_dir[0] * (arrow_size / 2))
    right_wing = (end_pos[0] - unit_dir[0] * arrow_size + unit_dir[1] * (arrow_size / 2),
                  end_pos[1] - unit_dir[1] * arrow_size - unit_dir[0] * (arrow_size / 2))
    pg.draw.polygon(screen, color, [end_pos, left_wing, right_wing])
