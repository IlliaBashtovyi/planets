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

# creation preview dict
creating = {'stage': 0, 'x': 0, 'y': 0, 'rad': 0, 'mouse_pos': (0, 0)}

# main loop
runing = True
while runing:
    # update live mouse position for preview
    mouse_pos = pg.mouse.get_pos()
    creating['mouse_pos'] = mouse_pos
    creating['stage'] = count
    creating['x'] = x
    creating['y'] = y
    creating['rad'] = rad

    # check for events
    for event in pg.event.get():
        # stop if escape is pressed
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            runing = False
        elif event.type == pg.QUIT:
            runing = False

        # set position of new object (first left click)
        if count == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pg.mouse.get_pos()
                rad = 0
                vx = vy = 0
                count = 1
                creating['x'], creating['y'] = x, y
        # set radius of new object (right click while previewing radius)
        elif count == 1:
            # update preview radius continuously
            if event.type == pg.MOUSEMOTION:
                rad = ph.dist_points(x, y, *pg.mouse.get_pos())
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                rad = ph.dist_points(x, y, *pg.mouse.get_pos())
                count = 2
        # set velocity of new object and create it (left click)
        elif count == 2:
            # update preview velocity vector continuously
            if event.type == pg.MOUSEMOTION:
                vx, vy = (pg.mouse.get_pos()[0] - x)/10, (pg.mouse.get_pos()[1] - y)/10
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                vx, vy = (pg.mouse.get_pos()[0] - x)/10, (pg.mouse.get_pos()[1] - y)/10
                lst.append(ph.OBJECT(x, y, rad, vx, vy))
                # reset creation state
                count = 0
                x = y = vx = vy = rad = 0
                creating = {'stage': 0, 'x': 0, 'y': 0, 'rad': 0, 'mouse_pos': (0, 0)}

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mult += 1
            if event.key == pg.K_DOWN:
                mult -=1

    # if user is in radius preview (mouse moved without event), update rad
    if count == 1:
        rad = ph.dist_points(x, y, *mouse_pos)
        creating['rad'] = rad
    if count == 2:
        # update creating mouse_pos already set above; preview velocity will be drawn by grafics
        pass

    # update physics
    # calculate acceleration
    for obj in lst:
        for other in lst:
            if obj != other:
                obj.acceler(other)
    # move objects
    for obj in lst:
        obj.move()

    # update graphics (pass creation preview)
    g.draw_objects(lst, mult, creating)

    # cap the frame rate (avoid passing 0)
    target_fps = max(1, mult * ph.time)
    clock.tick(target_fps)
