import gdspy
import math

from .Form import SimpleForm

class Cross(SimpleForm):

    def __init__(self, layer, cell, size, width, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.size = size
        self.width = width

        self.__createCross()

    def __createCross(self):
        s2 = self.size/2
        w2 = self.width/2

        arm1 = gdspy.Rectangle((-s2, -w2), (+s2, +w2))
        arm2 = gdspy.Rectangle((-w2, -s2), (+w2, +s2))

        self._add(gdspy.boolean(arm1, arm2, 'or', **self.layer))
