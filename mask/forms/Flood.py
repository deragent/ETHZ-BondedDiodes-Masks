import gdspy
import math

from .Form import SimpleForm

class Flood(SimpleForm):

    def __init__(self, layer, cell, A, B, radius=None, keepout=[], origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.A = A
        self.B = B

        self.radius = radius
        self.keepout = keepout

        self.__createRect()

    def __createRect(self):

        flood = gdspy.Rectangle(self.A, self.B, **self.layer)

        if self.radius is not None and self.radius > 0:
            cicrle = gdspy.Round((0, 0), self.radius, tolerance=10, **self.layer)
            flood = gdspy.boolean(flood, cicrle, 'and', **self.layer)

        for keepout in self.keepout:
            rect = gdspy.Rectangle(keepout[0], keepout[1], **self.layer)
            flood = gdspy.boolean(flood, rect, 'not', **self.layer)

        self._add(flood)
