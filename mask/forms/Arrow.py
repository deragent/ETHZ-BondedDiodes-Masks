import gdspy
import math

class MarkerArrow():

    def __init__(self, layer, cell, size, origin=(0,0), angle=0, offset=0):

        self.size = size
        self.offset = offset

        self.origin = origin
        self.angle = angle

        self.layer = layer
        self.cell = cell

        self.__createArrow()

    def __createArrow(self):
        s = self.size

        arrow = gdspy.Polygon([
            (0, 0), (5*s, 5*s), (5.2*s, 5*s), (5.2*s, 2.5*s), (13*s, 2.5*s),
            (13*s, -2.5*s), (5.2*s, -2.5*s), (5.2*s, -5*s), (5*s, -5*s),
        ])

        box = gdspy.Rectangle((14*s, -2.5*s), (18*s, 2.5*s))

        full = gdspy.boolean(arrow, box, 'or', **self.layer).rotate(self.angle).translate(*self.origin)
        if self.offset != 0:
            self.cell.add(gdspay.offset(full, self.offset, join='miter', join_first=True, **self.layer))
        else:
            self.cell.add(full)
