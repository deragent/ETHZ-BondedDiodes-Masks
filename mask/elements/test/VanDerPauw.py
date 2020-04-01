import gdspy
import math

from ...forms import VanDerPauwClover

from .. import Element

class VanDerPauwMetal(Element):

    def __init__(
        self, parent, name,
        radius=None, fraction=6, contactw=1000, contactspacing=2540,
        layers=None, lib=None
    ):

        if radius is None:
            radius = 0.5*math.sqrt(2)*(contactspacing + contactw)

        self.radius = radius
        self.fraction = fraction

        self.contactspacing = contactspacing
        self.contactw = contactw

        super().__init__(parent, name, layers, lib)

    def construct(self):

        c = VanDerPauwClover(
            self.layers["METALIZATION"], self.cell,
            self.radius, self.fraction
        )

        w = self.contactw
        for h in [-1, +1]:
            x = h * self.contactspacing/2
            for v in [-1, +1]:
                y = v * self.contactspacing/2

                self.cell.add(gdspy.Rectangle(
                    (x - w/2, y - w/2), (x + w/2, y + w/2),
                    **self.layers["PASSIVATION_OPEN"]
                ))



class VanDerPauwContact(Element):

    def __init__(self, parent, name, layers=None, lib=None):

        super().__init__(parent, name, layers, lib)

    def construct(self):
        pass
