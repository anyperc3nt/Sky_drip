import pygame
from pygame.draw import *

from settings import *


def init():
    global screen
    screen = pygame.display.set_mode((Xscreensize, Yscreensize))
    pygame.display.update()

    global layer_curr
    layer_curr = pygame.Surface((Xscreensize, Yscreensize))


def draw_star(coords, brightness):
    """отрисовывает звезду заданной яркости в точке x, y экрана"""

    brightness = int(brightness)

    print(brightness)

    x = coords[0]
    y = coords[1]

    circle(layer_curr, (brightness, brightness, brightness), (x, y), 1)


def update():
    global layer_curr

    screen.fill((0, 0, 0))

    pygame.Surface.blit(screen, layer_curr, (0, 0))

    pygame.display.update()

    # стирание слоя перед след кадром
    layer_curr.fill((0, 0, 0))
