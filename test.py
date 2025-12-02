import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Mouse Position Example")

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pg.mouse.get_pos()
            print(f"Mouse position: ({mouse_x}, {mouse_y})")

pg.quit()





