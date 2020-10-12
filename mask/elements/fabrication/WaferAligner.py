import gdspy
import math

from .. import Element

class WaferAligner(Element):

    def __init__(self, parent, name, xy, layer, size=1000, inverted=True, margin=1500, layers=None, lib=None):

        self.xy = xy

        self.layer = layer

        self.size = size

        self.inverted = inverted
        self.margin = margin

        super().__init__(parent, name, layers, lib)

    def construct(self):

        l = self.layers[self.layer]

        s = self.size

        x1 = self.xy[0]
        y1 = self.xy[1]

        x2 = x1 + math.copysign(s, x1)
        y2 = y1 + math.copysign(s, y1)

        rect = gdspy.Rectangle((x1, y1), (x2, y2), **l)

        if self.inverted:
            m = self.margin

            x1o = x1 - math.copysign(m, x1)
            y1o = y1 - math.copysign(m, y1)

            x2o = x2 + math.copysign(m, x1)
            y2o = y2 + math.copysign(m, y1)

            outer = gdspy.Rectangle((x1o, y1o), (x2o, y2o), **l)
            rect = gdspy.boolean(outer, rect, 'not', **l)


        self.cell.add(rect)
