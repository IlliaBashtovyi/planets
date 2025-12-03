import physics as f
import grafics as g
import pygame as pg


count = 0 # for creating objects
x, y, vx, vy, rad = 0, 0, 0, 0, 0  # parameters for new object
lst = []  # list of objects
# main loop
while True:
    # check for events
    for event in pg.event.get():
        # stop if escape is pressed
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            break
        # set position of new object
        if count == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                x, y = pg.mouse.get_pos()
                count += 1
        # set radius of new object
        if count == 1:
            if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                rad = f.dist_points(x, y, *pg.mouse.get_pos())
                count += 1
        # set velocity of new object and create it
        if count == 2:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                vx, vy = (pg.mouse.get_pos()[0] - x)/10, (pg.mouse.get_pos()[1] - y)/10
                lst.append(f.OBJECT(x, y, rad**2 * 1000, vx, vy))
                count = 0


# update physics
    # calculate acceleration
    for obj in lst:
        for other in lst:
            if obj != other:
                obj.acceler(other)
    # move objects
    for obj in lst:
        obj.move()

# update graphics
    g.draw_objects(lst)

# draw velocity arrows
if count == 2:
    g.arow((x, y), pg.mouse.get_pos() )


















