import gdspy

from .. import Element

from ...forms import GuardRings

class Diode(Element):

    def __init__(self, parent, name, size, overhang=10, layers=None, lib=None):

        try:
            self.A = size[0]
            self.B = size[1]
        except TypeError:
            self.A = size
            self.B = size

        self.overhang = overhang

        super().__init__(parent, name, layers, lib)

    def construct(self):
        self.__createDiode(self.layers["CONTACT_DOPING"], overhang = 0)
        self.__createDiode(self.layers["METALIZATION"], overhang = -self.overhang)
        self.__createGuardRings(self.layers["CONTACT_DOPING"], overhang = 0)
        self.__createGuardRings(self.layers["METALIZATION"], overhang = -self.overhang)

    def __createDiode(self, layer, overhang = 0):

        sA = self.A/2 + overhang
        sB = self.B/2 + overhang
        oh = overhang

        rect = gdspy.Rectangle((-sA, -sB), (sA, sB), **layer)

        self.cell.add(rect)

    def __createGuardRings(self, layer, overhang = 0):

        sA = self.A/2
        sB = self.B/2
        oh = overhang

        rect = gdspy.Rectangle((-sA, -sB), (sA, sB), **layer)

        GuardRings(layer, self.cell, rect, [
            (50-oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 100+2*oh)
        ])
