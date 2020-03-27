import gdspy
import math

class VanDerPauwClover():

    def __init__(self, layer, cell, radius, fraction, tolerance=1):

        self.radius = radius
        self.fraction = fraction

        self.cell = cell
        self.layer = layer
        self.tolerance = tolerance

        self.__createClover()

    def __createClover(self):
        r = self.radius
        w = int(self.radius/self.fraction)
        w2 = w/2

        full = gdspy.Round((0,0), r, tolerance=self.tolerance)

        for angle in [0, math.pi/2, math.pi, math.pi*3/2]:
            cutout = gdspy.Rectangle((w, -w2), (r+w, +w2)).rotate(angle)
            full = gdspy.boolean(full, cutout, 'not', **self.layer)

        self.cell.add(full)
