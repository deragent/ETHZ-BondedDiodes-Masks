import gdspy

from .. import Element

class Resistance(Element):

    WIDTH = 1000

    def __init__(self, parent, name, length, overhang=10, layers=None, lib=None):

        self.length = length
        self.overhang = overhang

        super().__init__(parent, name, layers, lib)

    def construct(self):

        oh = self.overhang

        w2 = self.WIDTH/2
        w2o = w2 + oh

        l2 = self.length/2
        lt2 = l2 + self.WIDTH + oh

        mw = 4*w2

        implant = gdspy.Rectangle((-lt2, -w2o), (lt2, w2o), **self.layers["CONTACT_DOPING"])

        contact1 = gdspy.Rectangle((-l2 - mw, -w2), (-l2, w2), **self.layers["METALIZATION"])
        contact2 = gdspy.Rectangle((l2, -w2), (l2 + mw, w2), **self.layers["METALIZATION"])

        open1a = gdspy.Rectangle((-l2 - mw + oh, -w2 + oh), (-l2 - oh, w2 - oh), **self.layers["PASSIVATION_OPEN"])
        open1b = gdspy.Rectangle((l2 + oh, -w2 + oh), (l2 + mw - oh, w2 - oh), **self.layers["PASSIVATION_OPEN"])

        self.cell.add(implant)
        self.cell.add(contact1)
        self.cell.add(contact2)

        self.cell.add(open1a)
        self.cell.add(open1b)
