import pygame
from pygame.draw import *

from settings import *


import pygame.freetype

"""
в качестве основных штук, с которыми этот модуль работает, имеет screen, 3 слоя для эффектов,
и один вспомогательный слой

layer_curr - слой, на котором отображается текущее расположение звезд на карте

layer_glow - слой, на котором отображаются увеличенные версии звезд, для дальнейшего их размытия 
и придания эффекта свечения

layer_motionblur - слой, на котором запоминаются все предыдущие расположения звезд, причем яркость
изображения на этом слое уменьшается каждый кадр путем наложения вспомогательного слоая layer_black,
что придает эффект плавного затухания
"""


def init():
    """функция инициализации модуля

    инициализирует дисплей в пайгейме
    создает необходимые для отрисовки объектов и эффектов слои
    """

    pygame.font.init()
    global myfont
    myfont = pygame.font.SysFont('Comic Sans MS', 30)






    global Xscreensize
    Xscreensize = int(pygame.display.Info().current_w)
    global Yscreensize
    Yscreensize = int(pygame.display.Info().current_h)
    print(Xscreensize)

    global screen
    #screen = pygame.display.set_mode((Xscreensize, Yscreensize))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.update()

    global layer_curr
    layer_curr = pygame.Surface((Xscreensize, Yscreensize))
    layer_curr = layer_curr.convert_alpha()
    layer_curr.fill((0, 0, 0, 0))

    global layer_glow
    layer_glow = pygame.Surface((Xscreensize, Yscreensize))
    layer_glow = layer_glow.convert_alpha()
    layer_glow.fill((0, 0, 0, 0))
    pygame.Surface.set_alpha(layer_glow, glow_brightness)

    global layer_motionblur
    layer_motionblur = pygame.Surface((Xscreensize, Yscreensize))
    layer_motionblur = layer_motionblur.convert_alpha()
    layer_motionblur.fill((0, 0, 0, 0))
    pygame.Surface.set_alpha(layer_motionblur, motionblur_brightness)

    # слой для реализации моушенблюра
    global layer_black
    layer_black = pygame.Surface((Xscreensize, Yscreensize))
    layer_black = layer_black.convert_alpha()
    layer_black.fill((0, 0, 0, 255-motionblur_force))


def draw_star(coords, name, brightness, visual_field, x_mouse, y_mouse):
    """отрисовывает звезду заданной яркости в точке x, y экрана

    coords - пара чисел (x,y)
    brightness - яркость от 0 до 255
    """


    eps = 4


    brightness = int(brightness)

    x = coords[0]
    y = coords[1]

    scale = 120/180*3.14/visual_field


    circle(layer_curr, (brightness, brightness, brightness), (x, y), scale)
    circle(layer_glow, (brightness, brightness, brightness), (x, y), scale*glow_size)
    if (x - x_mouse)**2 + (y-y_mouse)**2 < eps**2:
        return True
    else:
        return False


def update(x, y, name):
    """функция отображения нарисованной картинки на экран

    так же отображает и обрабатывает эффекты, такие как размытие звезд в движении, свечение звезд
    """
    global layer_curr
    global layer_motionblur
    global layer_glow

    textsurface = myfont.render(name, False, 'White')

    # тик обработки слоя размытия в движении
    pygame.Surface.blit(layer_motionblur, layer_black, (0, 0))
    pygame.Surface.blit(layer_motionblur, layer_curr, (0, 0))

    # тик обработки размытия звезд
    layer_glow = pygame.transform.smoothscale(
        layer_glow, (int(Xscreensize/glow_blur), int(Yscreensize/glow_blur)))
    layer_glow = pygame.transform.smoothscale(
        layer_glow, (Xscreensize, Yscreensize))

    # отрисовка слоев на экран
    screen.fill((0, 0, 0))
    pygame.Surface.blit(screen, layer_curr, (0, 0))
    pygame.Surface.blit(screen, layer_motionblur, (0, 0))
    pygame.Surface.blit(screen, layer_glow, (0, 0))

    textsurface1 = myfont.render(str(x)+" "+str(y), False, 'White')

    screen.blit(textsurface1, (0, 0))
    screen.blit(textsurface, (x, y))


    pygame.display.update()

    # стирание слоев перед след кадром
    layer_curr.fill((0, 0, 0, 0))
    layer_glow.fill((0, 0, 0, 0))

    #textsurface = myfont.render("", False, 'White')
