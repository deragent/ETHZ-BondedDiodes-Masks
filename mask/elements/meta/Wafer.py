import math

import gdspy

from .. import Element

class Wafer(Element):

    def __init__(self, parent, name, size, margin=5000, flat=57500, layers=None, lib=None):

        self.size = size
        self.margin = margin

        self.flat = flat

        super().__init__(parent, name, layers, lib)

    def construct(self):

        r = self.size/2
        f2 = self.flat/2

        bottom = math.sqrt(r**2 - f2**2)

        round = gdspy.Round((0, 0), r, tolerance=10)
        flat = gdspy.Rectangle((-r, -r*1.1), (r, -bottom))

        outline = gdspy.boolean(round, flat, 'not', **self.layers["WAFER_OUTLINE"])

        margin = gdspy.offset(outline, -self.margin, tolerance=100)

        wafer = gdspy.boolean(outline, margin, 'not', **self.layers["WAFER_OUTLINE"])

        # offset1 = gdspy.offset(self.base, offset + spec[0], join='round', tolerance=self.tolerance)
        # offset2 = gdspy.offset(self.base, offset + spec[0] + spec[1], join='round', tolerance=self.tolerance)
        #
        # diff = gdspy.boolean(offset2, offset1, 'not', **self.layers["WAFER_OUTLINE"])

        self.cell.add(wafer)
