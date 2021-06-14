import gdspy
import math

from .Form import SimpleForm

class Wheel(SimpleForm):

    def __init__(self, layer, cell, radius, division, radius_i=0, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.radius = radius
        self.radius_i = radius_i
        self.division = division

        self.__createWheel()

    def __createWheel(self):
        r = self.radius
        ri = self.radius_i

        d = self.division



        if ri > 0:
            circle = gdspy.Round((0, 0), r, inner_radius=ri, **self.layer)
        else:
            circle = gdspy.Round((0, 0), r, **self.layer)

        a = math.pi/d
        for dd in range(d):
            slice = gdspy.Round((0,0), r*1.1, initial_angle=a*2*dd, final_angle=a*(2*dd+1), **self.layer)
            # self._add(slice)
            circle = gdspy.boolean(circle, slice, 'not', **self.layer)

        self._add(circle)
