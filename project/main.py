import numpy as np
import pygame
import math

from pygame.version import ver

import data
import graphics
from settings import *


def conv_to_screen(phi, theta):
    """конвертирует угловые координаты звезды в координаты на экране

    phi, theta - углы по горизонтали и вертикали соответственно,
    должны лежать в диапозоне от -visual_field/2 до visual_field/2
    """

    x = (math.sin(phi)/math.sin(visual_field/2)+1)/2*graphics.Xscreensize
    y = (math.sin(theta)/math.sin(visual_field/2)+1)/2*graphics.Yscreensize

    return int(x), int(y)


pygame.init()
data.init()
graphics.init()

clock = pygame.time.Clock()
finished = False

FPS = 60

hor_angle = (0)/180*np.pi
vert_angle = (0)/180*np.pi

visual_field = 120/180*np.pi

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_UP]:
        vert_angle += 0.15/180*np.pi
    if keys[pygame.K_DOWN]:
        vert_angle -= 0.15/180*np.pi
    if keys[pygame.K_LEFT]:
        hor_angle += 0.15/180*np.pi
    if keys[pygame.K_RIGHT]:
        hor_angle -= 0.15/180*np.pi
    if keys[pygame.K_MINUS]:
        # проверка, чтобы область обзора была не больше 180
        if(visual_field < np.pi*0.9):
            visual_field *= 1.01
            print(visual_field)
    if keys[pygame.K_0]:
        visual_field /= 1.01

    visible_stars = data.what_we_see(hor_angle, vert_angle, visual_field)

    for star in visible_stars:
        graphics.draw_star(conv_to_screen(
            star.phi, star.theta), star.brightness)

    graphics.update()

pygame.quit()
