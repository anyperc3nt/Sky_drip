import numpy as np
import pygame
from pygame.constants import K_ESCAPE

import data
from graphics import *
from settings import *
import settings
from interface import *


pygame.init()
data.init()

graphics = Graphics()
interface = Interface(graphics)

clock = pygame.time.Clock()
finished = False
moving = False

FPS = 60

#горизонтальный и вертикальный угол поворота зрения
hor_angle = (0) / 180 * np.pi
vert_angle = (0) / 180 * np.pi

#поле зрения
visual_field = 60 / 180 * np.pi

Time = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE or event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                moving = True
                x, y = event.pos
                interface.check(x, y)
            elif event.button == 4:
                visual_field /= 1.09
            elif event.button == 5:
                if (visual_field < np.pi * 0.9):
                    visual_field *= 1.09

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            moving = False

        elif event.type == pygame.MOUSEMOTION:
            if moving:
                dx, dy = event.rel
                hor_angle -= visual_field * dx / graphics.Xscreensize
                vert_angle -= visual_field * dy / graphics.Yscreensize
    
    visible_stars = data.what_we_see(hor_angle, vert_angle, visual_field, Time)

    for star in visible_stars:
        graphics.draw_star(star, visual_field)

    interface.buttons_update()
    interface.information_update(
        [visual_field*180/np.pi, hor_angle*180/np.pi, vert_angle*180/np.pi, settings.time_speed])
    graphics.update()

    pygame.display.update()
    Time += 1 / 60 * settings.time_speed

pygame.quit()
