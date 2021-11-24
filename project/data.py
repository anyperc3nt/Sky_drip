import numpy as np
import pandas as pd


visual_field = np.pi*120/180


class Star:
    def __init__(self, phi, theta, brightness):
        self.phi = phi
        self.theta = theta
        self.brightness = brightness


def coord2angles(x, y, z):
    phi = np.arctan2(z, x) #horizontal
    theta = np.arctan2(y, np.sqrt(x**2+z**2)) #vertical
    return phi, theta


def initialise_stars():

    data_frame = pd.read_csv('hygdata_v3.csv')
    num_stars = len(data_frame)
    x = data_frame['x'].values
    y = data_frame['y'].values
    z = data_frame['z'].values
    phi, theta = coord2angles(x, y, z)
    mag = data_frame['mag'].values
    hundreds = np.array([100 for i in range(num_stars)])
    brightness = np.power(hundreds, mag / 5)

    stars = []

    for i in range(num_stars):
        stars.append(Star(phi[i], theta[i], brightness[i]))

    return stars


def what_we_see(hor_angle, vert_angle, stars):
    visible_stars = []

    for a_star in stars:
        if abs(a_star.phi - hor_angle) <= visual_field / 2 and abs(a_star.theta - vert_angle) <= visual_field / 2:
            visible_stars.append(a_star)

    return visible_stars

