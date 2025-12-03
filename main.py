import physics as ph
import grafics as g
import pygame as pg


# start graphics
g.start_graphics()

# to create consistent time steps
clock = pg.time.Clock()
mult = 1  # time multiplier
# for creating objects
count = 0
x, y, vx, vy, rad = 0, 0, 0, 0, 0  # parameters for new object
lst = [ph.OBJECT(400, 300, 10, 0, 0, 50000)]  # list of objects
# main loop
runing = True
while runing:
    # check for events
    for event in pg.event.get():
        # stop if escape is pressed
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            runing = False
        elif event.type == pg.QUIT:
            runing = False
        # set position of new object
        if count == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pg.mouse.get_pos()
                count += 1
        # set radius of new object
        if count == 1:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                rad = ph.dist_points(x, y, *pg.mouse.get_pos())
                count += 1
        # set velocity of new object and create it
        if count == 2:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                vx, vy = (pg.mouse.get_pos()[0] - x)/10, (pg.mouse.get_pos()[1] - y)/10
                lst.append(ph.OBJECT(x, y, rad, vx, vy))
                count = 0


        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mult += 1
            if event.key == pg.K_DOWN:
                mult -=1

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
    g.draw_objects(lst, mult)


    # cap the frame rate
    clock.tick(mult*ph.time) # time FPS



















