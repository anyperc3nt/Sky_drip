import pygame
from pygame.draw import *
from settings import *
import settings
import pygame.freetype
from data import Star_img

import numpy as np
import math


class Graphics(object):
    def __init__(self):
        """функция инициализации модуля

        инициализирует дисплей и шрифты в пайгейме
        создает необходимые для отрисовки объектов и эффектов слои
        """
        pygame.font.init()
        self.Xscreensize = int(pygame.display.Info().current_w)
        self.Yscreensize = int(pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.update()

        # слой для отображения звезд
        self.layer_curr = self.make_layer(self.Xscreensize, self.Yscreensize)  
        # слой для текста на экране
        self.layer_text = self.make_layer(self.Xscreensize, self.Yscreensize)
        # слой для свечения звезд
        self.layer_glow = self.make_layer(
            self.Xscreensize, self.Yscreensize, glow_brightness)
        # слой для моушенблюра звезд
        self.layer_motionblur = self.make_layer(
            self.Xscreensize, self.Yscreensize, motionblur_brightness)  
        # слой для затухания моушенблюра    
        self.layer_black = self.make_layer(self.Xscreensize, self.Yscreensize, 255, (
            0, 0, 0, 255 - motionblur_force))      

    def make_layer(self, x, y, alpha=255, color=(0, 0, 0, 0)):
        """вспомогательная функция для упрощения создания слоев"""
        layer = pygame.Surface((x, y))
        layer = layer.convert_alpha()
        layer.fill(color)
        if(alpha != 255):
            pygame.Surface.set_alpha(layer, alpha)
        return layer

    def draw_star(self, star, visual_field):
        """отрисовывает звезду

        star - объект типа Star_img
        visual_field - поле зрения, используется для масштаба
        """
        x1, y1, brightness, name, id = star

        x = x1 * self.Xscreensize
        y = y1 * self.Yscreensize

        lightness = ((brightness + 100) % 255)*(1 -
                                                int((brightness + 100)/255)) + 255 * int((brightness + 100)/255)

        scale = (brightness / 255 * 10) / visual_field
        if scale < 1:
            scale = 1

        circle(self.layer_curr, (lightness, lightness,
               lightness), (x, y), int(scale))
        # рисуем увеличенную версию звезды на слой glow
        if glow_on:
            circle(self.layer_glow, (lightness, lightness, lightness),
                   (x, y), int(scale * glow_size))
        if text_on:
            if name == name:  # not nan
                myfont = pygame.freetype.SysFont(
                    'Comic Sans MS', int(scale * 4))
                myfont.render_to(self.layer_text, (x, y), name,
                                 (lightness, lightness, lightness))

    def draw_text(self, text, x, y, w, h):
        """функция отрисовки текста для интерфейса"""
        myfont = pygame.freetype.SysFont('Comic Sans MS', int(h))
        text_surf = self.make_layer(w, h, 255, (0, 0, 0, 0))
        myfont.render_to(text_surf, (0, 0), text, (200, 255, 200))
        pygame.Surface.blit(self.layer_text, text_surf, (x, y))

    def glow_update(self):
        """функция обновления свечения звезд"""
        self.layer_glow = pygame.transform.smoothscale(
            self.layer_glow, (int(self.Xscreensize / glow_blur), int(self.Yscreensize / glow_blur)))
        self.layer_glow = pygame.transform.smoothscale(
            self.layer_glow, (self.Xscreensize, self.Yscreensize))
        pygame.Surface.blit(self.screen, self.layer_glow, (0, 0))
        self.layer_glow.fill((0, 0, 0, 0))

    def motionblur_update(self):
        """функция обновления размытия в движении"""
        pygame.Surface.blit(self.layer_motionblur, self.layer_black, (0, 0))
        pygame.Surface.blit(self.layer_motionblur, self.layer_curr, (0, 0))
        pygame.Surface.blit(self.screen, self.layer_motionblur, (0, 0))

    def stars_update(self):
        """функция обновления нарисованных звезд"""
        pygame.Surface.blit(self.screen, self.layer_curr, (0, 0))
        self.layer_curr.fill((0, 0, 0, 0))

    def text_update(self):
        """функция обновления текста"""
        pygame.Surface.blit(self.screen, self.layer_text, (0, 0))
        self.layer_text.fill((0, 0, 0, 0))

    def update(self):
        """функция отрисовки нарисованного кадра на экран"""
        self.screen.fill((0, 0, 0))

        if settings.motionblur_on:
            self.motionblur_update()

        if glow_on:
            self.glow_update()

        self.stars_update()

        if text_on:
            self.text_update()

        pygame.display.update()
