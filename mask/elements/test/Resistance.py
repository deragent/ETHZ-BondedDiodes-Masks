import gdspy

from .. import Element

from ...forms import GuardRings

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

        self.cell.add(implant)
        self.cell.add(contact1)
        self.cell.add(contact2)
