import gdspy

from .. import Element

class Mask(Element):

    def __init__(self, parent, name, size, margin=4000, layers=None, lib=None):

        self.size = size
        self.margin = margin

        super().__init__(parent, name, layers, lib)

    def construct(self):

        s2 = self.size/2
        s2m = self.size/2 - self.margin

        outer = gdspy.Rectangle((-s2, -s2), (s2, s2))
        inner = gdspy.Rectangle((-s2m, -s2m), (s2m, s2m))

        outline = gdspy.boolean(outer, inner, 'not', **self.layers["MASK_OUTLINE"])

        # offset1 = gdspy.offset(self.base, offset + spec[0], join='round', tolerance=self.tolerance)
        # offset2 = gdspy.offset(self.base, offset + spec[0] + spec[1], join='round', tolerance=self.tolerance)
        #
        # diff = gdspy.boolean(offset2, offset1, 'not', **self.layers["WAFER_OUTLINE"])

        os = self.margin / 5
        holes = [
            gdspy.Rectangle((-s2m, s2m+os), (s2m, s2-os)),
            gdspy.Rectangle((-s2m, -s2m-os), (s2m, -s2+os)),
            gdspy.Rectangle((s2m+os, -s2m), (s2-os, s2m)),
            gdspy.Rectangle((-s2m-os, -s2m), (-s2+os, s2m)),
        ]
        for hole in holes:
            outline = gdspy.boolean(outline, hole, 'not', **self.layers["MASK_OUTLINE"])

        self.cell.add(outline)
