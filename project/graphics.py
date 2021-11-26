import pygame
from pygame.draw import *

from settings import *


def init():
    global screen
    screen = pygame.display.set_mode((Xscreensize, Yscreensize))
    pygame.display.update()

    global layer_curr
    layer_curr = pygame.Surface((Xscreensize, Yscreensize))
    layer_curr = layer_curr.convert_alpha()
    layer_curr.fill((0,0,0,0))

    global layer_motionblur
    layer_motionblur = pygame.Surface((Xscreensize, Yscreensize))
    layer_motionblur = layer_motionblur.convert_alpha()
    layer_motionblur.fill((0,0,0,0))

    global layer_black
    layer_black = pygame.Surface((Xscreensize,Yscreensize))
    layer_black = layer_black.convert_alpha()
    layer_black.fill((0,0,0,80))


def draw_star(coords, brightness):
    """отрисовывает звезду заданной яркости в точке x, y экрана"""

    x = coords[0]
    y = coords[1]

    circle(layer_curr, (250, 250, 250), (x, y), 1)


def update():
    global layer_curr
    global layer_motionblur

    pygame.Surface.blit(layer_motionblur,layer_black,(0,0))
    pygame.Surface.blit(layer_motionblur,layer_curr,(0,0))
    pygame.Surface.set_alpha(layer_motionblur, 230)

    screen.fill((0, 0, 0))

    pygame.Surface.blit(screen, layer_curr, (0, 0))
    pygame.Surface.blit(screen, layer_motionblur, (0, 0))

    pygame.display.update()

    # стирание слоя перед след кадром
    layer_curr.fill((0, 0, 0,0))
