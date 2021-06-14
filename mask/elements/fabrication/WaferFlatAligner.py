import gdspy
import math

from .. import Element
from ...forms import ScaleBarVertical

class WaferFlatAligner(Element):

    def __init__(self, parent, name, size, flat, layer, height=2000, step=50, layers=None, lib=None):

        self.height = height
        self.size = size
        self.flat = flat

        self.y0 = -1*math.sqrt(self.size**2 - self.flat**2)/2

        self.step = step

        self.layer = layer

        super().__init__(parent, name, layers, lib)

    def construct(self):
        h = self.height
        step = self.step
        f2 = self.flat/2
        y0 = self.y0

        l = self.layers[self.layer]

        # Add the corner markers
        for x in (f2, -f2):
            x2 = x + math.copysign(h/2, x)
            y2 = y0 - h/2

            rect = gdspy.Rectangle((x, y0), (x2, y2), **l)

            self.cell.add(rect)

        # Add the vertical markers
        x = f2*0.9

        markers_left = ScaleBarVertical(
            l, self.cell, left=True,
            height=h, step=step,
            origin=(-x, y0)
        )

        markers_right = ScaleBarVertical(
            l, self.cell, left=False,
            height=h, step=step,
            origin=(x, y0)
        )
