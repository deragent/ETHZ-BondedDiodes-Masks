import gdspy

from .. import Element

from ...forms import GuardRings

class Diode(Element):

    def __init__(self, parent, name, size, rounding=0, window=0, overhang=10, layers=None, lib=None, tolerance=40):

        self.tolerance = 40

        try:
            self.A = size[0]
            self.B = size[1]
        except TypeError:
            self.A = size
            self.B = size

        self.overhang = overhang

        self.rounding = rounding if rounding > 0 else None
        self.window = window if window > 0 else None

        super().__init__(parent, name, layers, lib)

    def construct(self):
        self.__createDiode(self.layers["CONTACT_DOPING"], overhang = 0)
        self.__createDiode(self.layers["METALIZATION"], overhang = -self.overhang, window = self.window)
        self.__createGuardRings(self.layers["CONTACT_DOPING"], overhang = 0)
        self.__createGuardRings(self.layers["METALIZATION"], overhang = -self.overhang)

    def __createDiode(self, layer, overhang = 0, window=None):

        r = self.rounding if self.rounding is not None else 0

        sA = self.A/2 + overhang - r
        sB = self.B/2 + overhang - r
        oh = overhang

        rect = gdspy.Rectangle((-sA, -sB), (sA, sB), **layer)

        if self.rounding is None:
            form = rect
        else:
            form = gdspy.offset(rect, r, join='round', tolerance=self.tolerance, **layer)

        if window is not None:
            hole = gdspy.Round((0,0), window/2, tolerance=self.tolerance)
            form = gdspy.boolean(form, hole, 'not', **layer)

        self.cell.add(form)

    def __createGuardRings(self, layer, overhang = 0):

        r = self.rounding if self.rounding is not None else 0

        sA = self.A/2 - r
        sB = self.B/2 - r
        oh = overhang

        rect = gdspy.Rectangle((-sA, -sB), (sA, sB), **layer)

        GuardRings(layer, self.cell, rect, [
            (r + 50-oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 100+2*oh)
        ])
