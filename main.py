import physics as ph
import grafics as g
import pygame as pg


# start graphics (now resizable)
g.start_graphics()

# to create consistent time steps
clock = pg.time.Clock()
mult = 1  # time multiplier

# for creating objects
count = 0
x, y, vx, vy, rad = 0, 0, 0, 0, 0  # parameters for new object
lst = []  # list of objects

# for moving screen
dx, dy = 2, 2
up, down, left, right = False, False, False, False

# for zooming
zoom_in, zoom_out = False, False
zoom = 1

# camera (world coords at screen center)
cam_x, cam_y = 0.0, 0.0

# creation preview dict (x,y are world coords)
creating = {'stage': 0, 'x': 0, 'y': 0, 'rad': 0, 'mouse_pos': (0, 0)}

def screen_to_world(sx, sy, cam_x, cam_y, zoom):
    sw, sh = g.screen.get_size()
    wx = cam_x + (sx - sw/2) / zoom
    wy = cam_y + (sy - sh/2) / zoom
    return wx, wy

# main loop
runing = True
while runing:
    # update live mouse position for preview (screen coords)
    mouse_pos = pg.mouse.get_pos()
    creating['mouse_pos'] = mouse_pos
    creating['stage'] = count
    creating['x'] = x
    creating['y'] = y
    creating['rad'] = rad

    # check for events
    for event in pg.event.get():
        # stop if escape is pressed or window closed
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            runing = False
        elif event.type == pg.QUIT:
            runing = False

        # handle window resize
        if event.type == pg.VIDEORESIZE:
            # recreate screen at new size (keeps resizable flag)
            g.resize(event.w, event.h)

        # clear all objects if 'c' is pressed
        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            lst = []

        # handle keys
        if event.type == pg.KEYDOWN:
            # movement keys
            if event.key == pg.K_w:
                up = True
            if event.key == pg.K_s:
                down = True
            if event.key == pg.K_a:
                left = True
            if event.key == pg.K_d:
                right = True

            # zooming keys
            if event.key == pg.K_q:
                zoom_out = True
            if event.key == pg.K_e:
                zoom_in = True

        if event.type == pg.KEYUP:
            # movement keys
            if event.key == pg.K_w:
                up = False
            if event.key == pg.K_s:
                down = False
            if event.key == pg.K_a:
                left = False
            if event.key == pg.K_d:
                right = False

            # zooming keys
            if event.key == pg.K_q:
                zoom_out = False
            if event.key == pg.K_e:
                zoom_in = False

        # set position of new object (first left click) - convert screen -> world
        if count == 0:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                sx, sy = pg.mouse.get_pos()
                x, y = screen_to_world(sx, sy, cam_x, cam_y, zoom)
                rad = 0
                vx = vy = 0
                count = 1
                creating['x'], creating['y'] = x, y

        # set radius of new object (left click while previewing radius)
        elif count == 1:
            # update preview radius continuously (use world coords)
            if event.type == pg.MOUSEMOTION:
                mx, my = pg.mouse.get_pos()
                mwx, mwy = screen_to_world(mx, my, cam_x, cam_y, zoom)
                rad = ph.dist_points(x, y, mwx, mwy)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pg.mouse.get_pos()
                mwx, mwy = screen_to_world(mx, my, cam_x, cam_y, zoom)
                rad = ph.dist_points(x, y, mwx, mwy)
                count = 2

        # set velocity of new object and create it (left click)
        elif count == 2:
            # update preview velocity vector continuously
            if event.type == pg.MOUSEMOTION:
                mx, my = pg.mouse.get_pos()
                mwx, mwy = screen_to_world(mx, my, cam_x, cam_y, zoom)
                vx, vy = (mwx - x), (mwy - y)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pg.mouse.get_pos()
                mwx, mwy = screen_to_world(mx, my, cam_x, cam_y, zoom)
                vx, vy = (mwx - x), (mwy - y)
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
        mx, my = mouse_pos
        mwx, mwy = screen_to_world(mx, my, cam_x, cam_y, zoom)
        rad = ph.dist_points(x, y, mwx, mwy)
        creating['rad'] = rad

    # update physics
    # calculate acceleration
    for obj in lst:
        for other in lst:
            if obj != other:
                obj.acceler(other)
    # move objects
    for obj in lst:
        obj.move()

    # move camera (instead of moving objects)
    if up:
        cam_y -= dy / zoom
    if down:
        cam_y += dy / zoom
    if left:
        cam_x -= dx / zoom
    if right:
        cam_x += dx / zoom

    # zoom if needed (zoom around screen center)
    if zoom_in:
        zoom *= 1.01
    if zoom_out:
        zoom /= 1.01

    # update graphics (pass creation preview and camera)
    g.draw_objects(lst, mult, creating, cam=(cam_x, cam_y), zoom=zoom)

    # cap the frame rate (avoid passing 0)
    target_fps = max(1, mult * ph.time)
    clock.tick(target_fps)
