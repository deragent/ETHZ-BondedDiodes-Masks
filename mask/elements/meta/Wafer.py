import math

import gdspy

from .. import Element
from ...forms import Ring

class Wafer(Element):

    def __init__(self, parent, name, size, margin=5000, flat=57500, layers=None, lib=None):

        self.size = size
        self.margin = margin

        self.flat = flat

        super().__init__(parent, name, layers, lib)

    def construct(self):

        r = self.size/2

        ring = Ring(
            self.layers["WAFER_OUTLINE"], self.cell,
            r-self.margin, r, flat=self.flat
        )

        border = Ring(
            self.layers["WAFER_BORDER"], self.cell,
            r-100, r, flat=self.flat
        )
