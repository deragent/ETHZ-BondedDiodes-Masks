import gdspy

from .Form import SimpleForm

class TextList(SimpleForm):

    def __init__(self, layer, cell, text, height=2000, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.textheight = height
        self.text = text

        self._constructLabel()


    def _constructLabel(self):

        TH = self.textheight

        maxlabel = self._constructTextList(self.text.keys(), 0, 0)
        maxvalue = self._constructTextList(self.text.values(), maxlabel*1.3, 0)

        ## Create the border
        rect = gdspy.Rectangle(
            (-TH, -TH),
            (maxlabel*1.3 + maxvalue + TH, len(self.text)*TH*1.3 + TH),
            **self.layer
        )
        outset = gdspy.offset(rect, TH/2)

        self._add(gdspy.boolean(outset, rect, 'not', **self.layer))


    def _constructTextList(self, values, x, y):

        maxlength = 0

        for value in values:
            if len(value) > 0:
                t = gdspy.Text(value, self.textheight, position=(x, y), **self.layer)
                self._add(t)

                bbox = t.get_bounding_box()
                length = bbox[1,0] - bbox[0,0]
                if length > maxlength: maxlength = length

            y += self.textheight*1.3

        return maxlength
