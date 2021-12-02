import numpy as np
import pandas as pd
from collections import namedtuple

from settings import *


#class Star:
 #   def __init__(self, phi, theta, brightness):
  #      self.phi = phi
  #      self.theta = theta
   #     self.brightness = brightness


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
    hundreds = np.array([100 for i in range(num_stars)])
    brightness = np.power(hundreds, mag / 5).tolist()
    mag = mag.tolist()
    not_null_sum = 0
    not_null_counter = 0
    #for i in range(len(mag)):
     #   if mag[i] > 6.5:
      #      brightness[i] = 0
       # else:
        #    not_null_sum += brightness[i]
         #   not_null_counter += 1
    i = 0
    while i < len(mag):
        if mag[i] > 6.5:
            #print(i, len(brightness), len(phi), len(theta))
            del brightness[i]
            del mag[i]
            del phi[i]
            del theta[i]
            del names[i]
        else:
            i += 1
    #brightness = brightness * 255.0/(np.max(brightness) - np.min(brightness))
    scale = 255.0/np.mean(brightness)
    brightness = [min(255, i*scale) for i in brightness]

    num_stars = len(brightness)

    global Star
    Star = namedtuple('Star', ['phi', 'theta', 'brightness', 'name', 'id'])

    stars = []

    for i in range(num_stars):
        stars.append(Star(phi[i], theta[i], brightness[i], names[i], ids[i]))


def what_we_see(hor_angle, vert_angle, visual_field):
    global stars

    visible_stars = []

    for a_star in stars:
        if abs(a_star.phi - hor_angle) % (2*np.pi) <= visual_field / 2 and abs(a_star.theta - vert_angle) % (2*np.pi) <= visual_field / 2:
            visible_star = Star((a_star.phi - hor_angle) % (2*np.pi), (a_star.theta - vert_angle) % (2*np.pi), a_star.brightness, a_star.name, a_star.id)


            visible_stars.append(visible_star)

    return visible_stars
