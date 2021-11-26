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

    global layer_glow
    layer_glow = pygame.Surface((Xscreensize, Yscreensize))
    layer_glow = layer_glow.convert_alpha()
    pygame.Surface.set_alpha(layer_glow, glow_brightness)
    layer_glow.fill((0,0,0,0))

    global layer_motionblur
    layer_motionblur = pygame.Surface((Xscreensize, Yscreensize))
    layer_motionblur = layer_motionblur.convert_alpha()
    pygame.Surface.set_alpha(layer_motionblur, motionblur_brightness)
    layer_motionblur.fill((0,0,0,0))

    global layer_black
    layer_black = pygame.Surface((Xscreensize,Yscreensize))
    layer_black = layer_black.convert_alpha()
    layer_black.fill((0,0,0,255-motionblur_force))


def draw_star(coords, brightness):
    """отрисовывает звезду заданной яркости в точке x, y экрана"""

    brightness = int(brightness)

    x = coords[0]
    y = coords[1]

    circle(layer_curr, (brightness, brightness, brightness), (x, y), 1)
    circle(layer_glow, (brightness, brightness, brightness), (x, y), glow_size)




def update():
    global layer_curr
    global layer_motionblur
    global layer_glow

    #тик обработки слоя размытия в движении
    pygame.Surface.blit(layer_motionblur,layer_black,(0,0))
    pygame.Surface.blit(layer_motionblur,layer_curr,(0,0))
    

    #тик обработки размытия звезд
    layer_glow=pygame.transform.smoothscale(layer_glow,(int(Xscreensize/glow_blur),int(Yscreensize/glow_blur)))
    layer_glow=pygame.transform.smoothscale(layer_glow,(Xscreensize,Yscreensize))

    #отрисовка слоев на экран
    screen.fill((0, 0, 0))
    pygame.Surface.blit(screen, layer_curr, (0, 0))
    pygame.Surface.blit(screen, layer_motionblur, (0, 0))
    pygame.Surface.blit(screen, layer_glow, (0, 0))

    pygame.display.update()

    # стирание слоя перед след кадром
    layer_curr.fill((0, 0, 0,0))
    layer_glow.fill((0, 0, 0,0))
