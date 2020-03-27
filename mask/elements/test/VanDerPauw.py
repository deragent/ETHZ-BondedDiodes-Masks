import gdspy

from ...forms import VanDerPauwClover

from .. import Element

class VanDerPauwMetal(Element):

    def __init__(self, parent, name, radius, fraction=6, layers=None, lib=None):

        self.radius = radius
        self.fraction = fraction

        super().__init__(parent, name, layers, lib)

    def construct(self):

        c = VanDerPauwClover(
            self.layers["METALIZATION"], self.cell,
            self.radius, self.fraction
        )


class VanDerPauwContact(Element):

    def __init__(self, parent, name, layers=None, lib=None):

        super().__init__(parent, name, layers, lib)

    def construct(self):
        pass
