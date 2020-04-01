import gdspy
import math

from .Form import SimpleForm

class MarkerArrow(SimpleForm):

    def __init__(self, layer, cell, size, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.size = size

        self.__createArrow()

    def __createArrow(self):
        s = self.size

        arrow = gdspy.Polygon([
            (0, 0), (5*s, 5*s), (5.2*s, 5*s), (5.2*s, 2.5*s), (13*s, 2.5*s),
            (13*s, -2.5*s), (5.2*s, -2.5*s), (5.2*s, -5*s), (5*s, -5*s),
        ])

        box = gdspy.Rectangle((14*s, -2.5*s), (18*s, 2.5*s))

        self._add(gdspy.boolean(arrow, box, 'or', **self.layer))
