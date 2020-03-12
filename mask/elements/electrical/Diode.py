import gdspy

from ...config import GLOBAL_LAYERS
from ...forms import GuardRings

class Diode():

    def __init__(self, lib, name, size, overhang=10, layers=GLOBAL_LAYERS):

        self.cell = lib.new_cell(name)
        self.layers = layers

        try:
            self.A = size[0]
            self.B = size[1]
        except TypeError:
            self.A = size
            self.B = size

        self.__createDiode(self.layers["CONTACT_DOPING"], overhang = overhang)
        self.__createDiode(self.layers["METALIZATION"], overhang = 0)

    def __createDiode(self, layer, overhang = 0):

        sA = self.A/2 + overhang
        sB = self.B/2 + overhang
        oh = overhang

        rect = gdspy.Rectangle((-sA, -sB), (sA, sB), **layer)

        GuardRings(layer, self.cell, rect, [
            (50-2*oh, 100+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 50+2*oh),
            (50-2*oh, 100+2*oh)
        ])

        self.cell.add(rect)
