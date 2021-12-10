import numpy as np
import pygame
import math
from pygame.constants import K_ESCAPE

from pygame.version import ver

import data
import graphics
from settings import *

def conv_to_screen(phi, theta):
    """конвертирует угловые координаты звезды в координаты на экране

    phi, theta - углы по горизонтали и вертикали соответственно,
    должны лежать в диапозоне от -visual_field/2 до visual_field/2
    """

    x = (math.tan(phi)/math.tan(visual_field/2)+1)/2*graphics.Xscreensize
    y = (math.tan(theta)/math.tan(visual_field/2)+1)/2*graphics.Yscreensize

    return int(x), int(y)


pygame.init()
data.init()
graphics.init()

clock = pygame.time.Clock()
finished = False
moving = False

FPS = 60

hor_angle = (0)/180*np.pi
vert_angle = (0)/180*np.pi

visual_field = 90/180*np.pi

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE or event.type == pygame.QUIT:
             finished = True 

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               moving = True
            elif event.button == 4:
                visual_field /= 1.09
            elif event.button == 5:
                if(visual_field < np.pi*0.9):
                    visual_field *= 1.09
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moving = False

        elif event.type == pygame.MOUSEMOTION:
            if moving:
                dx, dy = event.rel
                hor_angle -= visual_field*dx/graphics.Xscreensize
                vert_angle -= visual_field*dy/graphics.Yscreensize
        
               
    visible_stars = data.what_we_see(hor_angle, vert_angle, visual_field)

    for star in visible_stars:
        graphics.draw_star(conv_to_screen(star.phi, star.theta), star.name, star.id, star.brightness, visual_field)

    graphics.update()

pygame.quit()
