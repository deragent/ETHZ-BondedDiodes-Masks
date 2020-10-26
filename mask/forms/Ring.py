import gdspy
import math

from .Form import SimpleForm

class Ring(SimpleForm):

    def __init__(self, layer, cell, inner_radius, outer_radius, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

        self.__createArrow()

    def __createArrow(self):
        ri = self.inner_radius
        ro = self.outer_radius

        outer = gdspy.Round((0, 0), ro, tolerance=10, **self.layer)
        inner = gdspy.offset(outer, -(ro - ri), join_first=True, tolerance=10, **self.layer)

        self._add(gdspy.boolean(outer, inner, 'not', **self.layer))
