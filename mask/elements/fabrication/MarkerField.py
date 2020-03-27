import gdspy
import math

from .. import Element

from . import MarkerCoarse
from ...forms import MarkerArrow

class MarkerField(Element):

    def __init__(self, parent, name, config, arrowsize=20, layers=None, lib=None):

        self.config = config
        self.arrowsize = arrowsize

        super().__init__(parent, name, layers, lib)

    def construct(self):

        offset = 0
        layers = []

        for number, l1, l2, size in self.config:

            marker = MarkerCoarse(None, 'MARKER_%s_%s'%(l1, l2), number,
                l1, l2, size=size,
                layers=self.layers, lib=self.lib)

            self.cell.add(gdspy.CellReference(
                marker.cell,
                origin=(offset, 0)
            ))

            layers.extend([l1, l2])

            offset += marker.width*1.5

        self.__addArrows(set(layers))

    def __addArrows(self, layers):

        bbox = self.cell.get_bounding_box()

        xmin = bbox[0,0]
        xmax = bbox[1,0]

        ymin = bbox[0,1]
        ymax = bbox[1,1]

        mid_x = (xmax + xmin)/2
        mid_y = (ymax + ymin)/2

        s = self.arrowsize

        d = 40*s
        off = 30*s

        ## Horizontal arrows
        self._addArrow(xmax + d, mid_y, 0, layers)
        self._addArrow(xmin - d, mid_y, math.pi, layers)

        off_y = off
        while mid_y + off_y < ymax:
            self._addArrow(xmax + d, mid_y + off_y, 0, layers)
            self._addArrow(xmin - d, mid_y + off_y, math.pi, layers)

            self._addArrow(xmax + d, mid_y - off_y, 0, layers)
            self._addArrow(xmin - d, mid_y - off_y, math.pi, layers)

            off_y += off


        self._addArrow(mid_x, ymax + d, math.pi/2, layers)
        self._addArrow(mid_x, ymin - d, math.pi*3/2, layers)

        off_x = off
        while mid_x + off_x < xmax:
            self._addArrow(mid_x + off_x, ymax + d, math.pi/2, layers)
            self._addArrow(mid_x + off_x, ymin - d, math.pi*3/2, layers)

            self._addArrow(mid_x - off_x, ymax + d, math.pi/2, layers)
            self._addArrow(mid_x - off_x, ymin - d, math.pi*3/2, layers)

            off_x += off


        ## 45 deg angle
        self._addArrow(xmax + d, ymax + off, math.pi/4, layers)
        self._addArrow(xmin - d, ymax + off, math.pi*3/4, layers)

        self._addArrow(xmax + d, ymin - off, math.pi*7/4, layers)
        self._addArrow(xmin - d, ymin - off, math.pi*5/4, layers)



    def _addArrow(self, x, y, rotation, layers):

        for layer in layers:
            a = MarkerArrow(
                self.layers[layer], self.cell,
                self.arrowsize,
                (x, y), rotation
            )
