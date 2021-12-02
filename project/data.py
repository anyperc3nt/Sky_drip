import numpy as np
from numpy.lib.index_tricks import s_
import pandas as pd
from collections import namedtuple

from settings import *


#class Star:
 #   def __init__(self, phi, theta, brightness):
  #      self.phi = phi
  #      self.theta = theta
   #     self.brightness = brightness

Star = namedtuple('Star', ['phi', 'theta', 'brightness', 'name', 'id'])


def coord2angles(x, y, z):
    phi = np.arctan2(z, x)  # horizontal
    theta = np.arctan2(y, np.sqrt(x**2+z**2))  # vertical (declination)
    return phi, theta


def init():
    """инициализация модуля, загружает данные из файла с данными в глобальный массив stars"""

    global stars

    data_frame = pd.read_csv(__file__[:-7]+'hygdata_v3.csv')

    num_stars = len(data_frame)
    x = data_frame['x'].values
    y = data_frame['y'].values
    z = data_frame['z'].values
    names = data_frame['proper'].values.tolist()
    ids = data_frame['id'].values.tolist()
    phi, theta = coord2angles(x, y, z)
    phi = phi.tolist()
    theta = theta.tolist()
    mag = data_frame['mag'].values
    mag = mag.tolist()

    stars = []

    #самая яркая звезда сириус, у нее магнитуда -1,67
    #по этому мы берем -mag от -6,5 до 1,67
    #а еще я не беру звезды ярче сириуса, потому что в датасете походу есть солнце и другие слишком яркие объекты

    for i in range(num_stars):
        if((-mag[i]) > -6.5) and (-mag[i] < 1.68):
            s_brightness = (6.5 - mag[i])/(1.68+6.5)*255
            stars.append(Star(phi[i], theta[i], s_brightness, names[i], ids[i]))


def what_we_see(hor_angle, vert_angle, visual_field):
    """возвращает относительные угловые координаты звезд, находящихся в угловом диапозоне видимости
    
    hor_angle, vert_angle - углы направления зрения пользователя в радианах
    visual_field - угол обзора пользователя
    """
    global stars

    visible_stars = []

    for a_star in stars:
        if abs(a_star.phi - hor_angle) % (2*np.pi) <= visual_field / 2 and abs(a_star.theta - vert_angle) % (2*np.pi) <= visual_field / 2:
            visible_star = Star((a_star.phi - hor_angle) % (2*np.pi), (a_star.theta - vert_angle) % (2*np.pi), a_star.brightness, a_star.name, a_star.id)

            visible_stars.append(visible_star)

    return visible_stars
