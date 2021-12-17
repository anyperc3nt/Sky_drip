import numpy as np
from numpy.lib.index_tricks import s_
import pandas as pd
from collections import namedtuple
import math

#тапл для хранения данных о звездах
Star = namedtuple('Star', ['phi', 'theta', 'brightness', 'name', 'id'])
#тапл для передаче графиге данных о звездах
Star_img = namedtuple('Star', ['x1', 'y1', 'brightness', 'name', 'id'])
# x1, y1 = линейные координаты звезд, нормированные к еденице


def coord2angles(x, y, z):
    """конвертирует трехмерные координаты в полярные"""
    phi = np.arctan2(z, x)  # horizontal
    theta = np.arctan2(y, np.sqrt(x ** 2 + z ** 2))  # vertical (declination)
    return phi, theta


def init():
    """инициализация модуля, загружает данные из файла с данными в глобальный массив stars"""

    global stars

    data_frame = pd.read_csv(__file__[:-7] + 'hygdata_v3.csv')

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

    """
    самая яркая звезда сириус, у нее магнитуда -1,67
    по этому мы берем -mag от -6,5 до 1,67
    а еще не берем звезды ярче сириуса, потому что в датасете видимо есть солнце и другие слишком яркие объекты
    """

    for i in range(num_stars):
        if ((-mag[i]) > -6.5) and (-mag[i] < 1.68):
            s_brightness = (6.5 - mag[i]) / (1.68 + 6.5) * 255
            stars.append(
                Star(phi[i], theta[i], s_brightness, names[i], ids[i]))


def what_we_see(hor_angle, vert_angle, visual_field, Time):
    """возвращает относительные угловые координаты звезд, находящихся в угловом диапозоне видимости

    hor_angle, vert_angle - углы направления зрения пользователя в радианах
    visual_field - угол обзора пользователя
    Time - время, от него зависит расположение звезд
    """
    global stars

    delta_w = 0.00001
    delta_h = 0.00001

    visible_stars = []

    for a_star in stars:
        theta = a_star.theta - vert_angle + delta_h*Time
        phi = a_star.phi - hor_angle + delta_w*Time
        x1 = (math.tan(phi) / math.tan(visual_field / 2) + 1) / 2
        y1 = (math.tan(theta) / math.tan(visual_field / 2) + 1) / 2

        if 0 <= x1 <= 1 and 0 <= y1 <= 1:
            visible_star = Star_img(
                x1, y1, a_star.brightness, a_star.name, a_star.id)
            visible_stars.append(visible_star)

    return visible_stars
