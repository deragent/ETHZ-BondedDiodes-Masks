import gdspy

from .. import Element

class Wafer(Element):

    def __init__(self, parent, name, size, margin=5000, layers=None, lib=None):

        self.size = size
        self.margin = margin
        
        super().__init__(parent, name, layers, lib)

    def construct(self):

        flat_cut = 8000

        round = gdspy.Round((0, 0), self.size/2, tolerance=10)
        flat = gdspy.Rectangle((-self.size/2, -self.size/2*1.1), (self.size/2, -self.size/2 + flat_cut))

        outline = gdspy.boolean(round, flat, 'not', **self.layers["WAFER_OUTLINE"])

        margin = gdspy.offset(outline, -self.margin, tolerance=100)

        wafer = gdspy.boolean(outline, margin, 'not', **self.layers["WAFER_OUTLINE"])

        # offset1 = gdspy.offset(self.base, offset + spec[0], join='round', tolerance=self.tolerance)
        # offset2 = gdspy.offset(self.base, offset + spec[0] + spec[1], join='round', tolerance=self.tolerance)
        #
        # diff = gdspy.boolean(offset2, offset1, 'not', **self.layers["WAFER_OUTLINE"])

        self.cell.add(wafer)
