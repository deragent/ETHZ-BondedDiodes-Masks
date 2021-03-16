import numpy as np

class Outline():

    def __init__(self, size, flat=57500):

        self.r = size/2
        self.flat = flat

        self.ymin = -np.sqrt(self.r**2 - (self.flat/2)**2)

    def xMaxAtY(self, y):

        if y > self.r or y < -self.r:
            return None

        if y < self.ymin:
            return None

        return np.sqrt(self.r**2 - y**2)

    def xMinAtY(self, y):
        return -1*self.xMaxAtY(y)

    def yMaxAtX(self, x):

        if x > self.r or x < -self.r:
            return None

        return np.sqrt(self.r**2 - x**2)

    def yMinAtX(self, x):

        y = -1*self.yMaxAtX(x)

        if y < self.ymin:
            return self.ymin
        else:
            return y
