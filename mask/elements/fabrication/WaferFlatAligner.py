import gdspy
import math

from .. import Element

class WaferFlatAligner(Element):

    def __init__(self, parent, name, size, flat, layer, height=2000, step=50, inverted=True, layers=None, lib=None):

        self.height = height
        self.size = size
        self.flat = flat

        self.y0 = -1*math.sqrt(self.size**2 - self.flat**2)/2

        self.step = step

        self.layer = layer

        self.inverted = inverted

        self._elements = []

        super().__init__(parent, name, layers, lib)

    def __add(self, element):
        self._elements.append(element)

    def drawElements(self):

        if self.inverted:
            l = self.layers[self.layer]

            y0 = self.y0
            h = self.height
            f2 = self.flat/2

            base = gdspy.Rectangle((-f2*1.1, y0 - h*1.1), (f2*1.1, y0 + h*1.1), **l)

            for element in self._elements:
                base = gdspy.boolean(base, element, 'not', **l)

            self.cell.add(base)

        else:
            for element in self._elements:
                self.cell.add(element)

    def addBar(self, offset, x, label=False):
        l = self.layers[self.layer]

        y0 = self.y0
        w = self.step / 5

        bl = 10*w if not label else 20*w

        rect = gdspy.Rectangle((x, y0 + offset - w), (x + math.copysign(bl, x), y0 + offset + w), **l)

        if label:
            th = 4*self.step
            to = 30*w
            if x < 0:
                to = -1*to - len(str(offset))*th*8/9

            text = gdspy.Text(str(offset), th, position=(x + to, y0 + offset - th/2), **l)
            self.__add(text)

        self.__add(rect)

    def construct(self):
        h = self.height
        step = self.step
        f2 = self.flat/2
        y0 = self.y0

        l = self.layers[self.layer]

        # Add the cornver markers
        for x in (f2, -f2):
            x2 = x + math.copysign(h/2, x)
            y2 = y0 - h/2

            rect = gdspy.Rectangle((x, y0), (x2, y2), **l)

            self.__add(rect)

        # Add the vertical markers
        x = f2 * 0.9

        offset = 0
        ii = 0
        self.addBar(offset, x, label=True)
        self.addBar(offset, -x, label=True)

        while offset+step < h*0.9:
            offset += step
            ii += 1
            label = (ii % 5 == 0)

            self.addBar(offset, x, label=label)
            self.addBar(offset, -x, label=label)
            self.addBar(-offset, x, label=label)
            self.addBar(-offset, -x, label=label)

        self.drawElements()
