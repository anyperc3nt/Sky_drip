import numpy as np
import pygame
import math

from pygame.version import ver

import data
import graphics
from settings import *


def conv_to_screen(phi, tetta, visual_field):
    """конвертирует угловые координаты звезды в координаты на экране"""

    x = math.sin(phi)*Xscreensize/math.sin(visual_field/2)
    y = math.sin(tetta)*Yscreensize/math.sin(visual_field/2)

    return int(x), int(y)


pygame.init()
data.init()
print("data initialisation complete")
graphics.init()
print("graphics initialisation complete")

clock = pygame.time.Clock()
finished = False

FPS = 60

hor_angle = (0)/180*np.pi
vert_angle = (0)/180*np.pi

visual_field = 20/180*np.pi

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == 119:
                vert_angle -= 4/180*np.pi
                print("вертикальный угол ", vert_angle/np.pi*180)
            elif event.key == 115:
                vert_angle += 4/180*np.pi
                print("вертикальный угол ", vert_angle/np.pi*180)
            elif event.key == 100:
                hor_angle += 4/180*np.pi
                print("горизонтальный угол ", hor_angle/np.pi*180)
            elif event.key == 97:
                hor_angle -= 4/180*np.pi
                print("горизонтальный угол ", hor_angle/np.pi*180)
            elif event.key == 113:
                visual_field *= 1.3
                print("угол обзора ", visual_field/np.pi*180)
            elif event.key == 101:
                visual_field /= 1.3
                print("угол обзора ", visual_field/np.pi*180)
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEMOTION:
            pass

    visible_stars = data.what_we_see(hor_angle, vert_angle, visual_field)

    for star in visible_stars:
        graphics.draw_star(conv_to_screen(
            star.phi, star.theta, visual_field), star.brightness)

    graphics.update()

pygame.quit()
