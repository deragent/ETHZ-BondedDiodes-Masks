import gdspy
import math

from .Form import SimpleForm

class ScaleBarVertical(SimpleForm):

    def __init__(self, layer, cell, left=True, height=2000, step=50, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.height = height
        self.left = left
        self.step = step

        self._constructScale();


    def _addBar(self, offset, label=False):
        l = self.layer

        orientation = -1 if self.left else 1

        w = self.step / 5
        bl = 10*w if not label else 20*w

        rect = gdspy.Rectangle((0, offset - w), (orientation*bl, offset + w), **l)

        if label:
            th = 4*self.step
            to = 30*w
            if orientation < 0:
                to = -1*to - len(str(offset))*th*8/9

            text = gdspy.Text(str(offset), th, position=(to, offset - th/2), **l)
            self._add(text)

        self._add(rect)

    def _constructScale(self):
        h = self.height
        step = self.step

        ii = 0
        self._addBar(0, label=True)

        while (ii+1)*step < h*0.9:
            ii += 1
            label = (ii % 5 == 0)

            self._addBar(ii*step, label=label)
            self._addBar(-ii*step, label=label)
