import pygame
from pygame.draw import *
from settings import *
import pygame.freetype
from data import Star_img

"""
в качестве основных штук, с которыми этот модуль работает, имеет screen, 3 слоя для эффектов

layer_curr - слой, на котором отображается текущее расположение звезд на карте

layer_glow - слой, на котором отображаются увеличенные версии звезд, для дальнейшего их размытия 
и придания эффекта свечения

layer_motionblur - слой, на котором запоминаются все предыдущие расположения звезд, причем яркость
изображения на этом слое уменьшается каждый кадр путем наложения вспомогательного слоя layer_black,
что придает эффект плавного затухания
"""


def init():
    """функция инициализации модуля

    инициализирует дисплей в пайгейме
    создает необходимые для отрисовки объектов и эффектов слои
    """
    pygame.font.init()
    # global myfont
    # myfont = pygame.freetype.SysFont('Comic Sans MS', 10)
    global Xscreensize
    Xscreensize = int(pygame.display.Info().current_w)
    global Yscreensize
    Yscreensize = int(pygame.display.Info().current_h)
    print(Xscreensize)

    global screen
    # screen = pygame.display.set_mode((Xscreensize, Yscreensize))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.update()

    global layer_curr
    layer_curr = pygame.Surface((Xscreensize, Yscreensize))
    layer_curr = layer_curr.convert_alpha()
    layer_curr.fill((0, 0, 0, 0))

    global layer_text
    layer_text = pygame.Surface((Xscreensize, Yscreensize))
    layer_text = layer_text.convert_alpha()
    layer_text.fill((0, 0, 0, 0))

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
    layer_black.fill((0, 0, 0, 255 - motionblur_force))


def draw_star(star, visual_field):
    """отрисовывает звезду заданной яркости в точке x, y экрана

    coords - пара чисел (x,y)
    brightness - яркость от 0 до 255
    """
    x1, y1, brightness, name, id = star


    brightness = int(brightness)

    x = x1 * Xscreensize
    y = y1 * Yscreensize


    scale = 120 / 180 * 3.14 / visual_field
    scale *= 5 * brightness / 255 + 1
    if scale < 1:
        scale = 1

    if brightness > 155:
        lightness = 255
    else:
        lightness = brightness + 100

    circle(layer_curr, (lightness, lightness, lightness), (x, y), int(scale))
    # рисуем увеличенную версию звезды на слой glow
    if glow_on:
        circle(layer_glow, (lightness, lightness, lightness), (x, y), int(scale * glow_size))
    if text_on:
        if name == name:  # not nan
            myfont = pygame.freetype.SysFont('Comic Sans MS', int(scale * 4))
            myfont.render_to(layer_text, (x, y), name, (255, 255, 255))


def glow_update():
    global layer_glow
    layer_glow = pygame.transform.smoothscale(layer_glow, (int(Xscreensize / glow_blur), int(Yscreensize / glow_blur)))
    layer_glow = pygame.transform.smoothscale(layer_glow, (Xscreensize, Yscreensize))
    pygame.Surface.blit(screen, layer_glow, (0, 0))
    layer_glow.fill((0, 0, 0, 0))


def motionblur_update():
    global layer_motionblur
    pygame.Surface.blit(layer_motionblur, layer_black, (0, 0))
    pygame.Surface.blit(layer_motionblur, layer_curr, (0, 0))
    pygame.Surface.blit(screen, layer_motionblur, (0, 0))


def stars_update():
    global layer_curr
    pygame.Surface.blit(screen, layer_curr, (0, 0))
    layer_curr.fill((0, 0, 0, 0))


def text_update():
    global layer_text
    pygame.Surface.blit(screen, layer_text, (0, 0))

    layer_text.fill((0, 0, 0, 0))


def update():
    """функция отрисовки нарисованного кадра на экран"""
    screen.fill((0, 0, 0))

    if motionblur_on:
        motionblur_update()

    if glow_on:
        glow_update()

    stars_update()

    if text_on:
        text_update()

    pygame.display.update()