import gdspy

from .. import Element

class Mask(Element):

    def __init__(self, parent, name, size, text, margin=4000, layers=None, lib=None):

        self.size = size
        self.margin = margin
        self.text = text

        super().__init__(parent, name, layers, lib)

    def construct(self):

        self._constructFrame()

        if len(self.text) > 0:
            self._constructLabel()

    def _constructFrame(self):
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


    def _constructLabel(self):
        T_HEIGHT = 2000

        x0 = -self.size/2 + 3*self.margin
        y0 = -self.size/2 + 3*self.margin

        text = self.lib.new_cell(self.name + '_LABEL')

        maxlabel = 0
        y = y0

        for label, value in self.text.items():
            t = gdspy.Text(label, T_HEIGHT, position=(x0, y), **self.layers["MASK_LABEL"])
            text.add(t)

            bbox = t.get_bounding_box()
            length = bbox[1,0] - bbox[0,0]
            if length > maxlabel: maxlabel = length

            y += T_HEIGHT*1.3

        maxvalue = 0
        y = y0

        for label, value in self.text.items():
            t = gdspy.Text(value, T_HEIGHT, position=(x0 + maxlabel*1.3, y), **self.layers["MASK_LABEL"])
            text.add(t)

            bbox = t.get_bounding_box()
            length = bbox[1,0] - bbox[0,0]
            if length > maxvalue: maxvalue = length

            y += T_HEIGHT*1.3

        rect = gdspy.Rectangle(
            (x0 - T_HEIGHT, y0 - T_HEIGHT),
            (x0 + maxlabel*1.3 + maxvalue + T_HEIGHT, y0 + len(self.text)*T_HEIGHT*1.3 + T_HEIGHT),
            **self.layers["MASK_LABEL"]
        )
        outset = gdspy.offset(rect, T_HEIGHT/2)

        text.add(gdspy.boolean(outset, rect, 'not', **self.layers["MASK_LABEL"]))

        self.cell.add(text)
