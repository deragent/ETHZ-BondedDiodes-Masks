import gdspy
import math

from ...forms import VanDerPauwClover
from ...forms import Cross

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

    def __init__(
        self, parent, name,
        contactw=1000, contactspacing=2540,
        overhang=10,
        layers=None, lib=None
    ):

        self.contactspacing = contactspacing
        self.contactw = contactw
        self.overhang = overhang

        super().__init__(parent, name, layers, lib)

    def construct(self):

        s = self.contactspacing + self.contactw

        cross = Cross(
            self.layers["CONTACT_DOPING"], self.cell,
            s, s/10
        )

        w2 = self.contactw/2
        for h in [-1, +1]:
            x = h * self.contactspacing/2
            for v in [-1, +1]:
                y = v * self.contactspacing/2

                ## TODO make offset customizable
                oh = self.overhang

                contact = gdspy.Rectangle((-w2-oh, -w2-oh), (w2+oh, +w2+oh))
                arm = gdspy.FlexPath([(0,0), (-0.55*self.contactspacing, 0)], 2*w2/5).translate(0, 3*w2/5)

                contact = gdspy.boolean(contact, arm, 'or', **self.layers["METALIZATION"])
                contact = contact.rotate(math.pi/2*((x != y) + (y < 0)*2))

                self.cell.add(contact.translate(x, y))

                self.cell.add(gdspy.Rectangle(
                    (-w2, -w2), (w2, w2),
                    **self.layers["PASSIVATION_OPEN"]
                ).translate(x, y))
