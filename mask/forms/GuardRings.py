import gdspy

class GuardRings():

    def __init__(self, layer, cell, base, specs, tolerance=40):

        if len(specs) == 2:
            specs = [specs]

        self.cell = cell
        self.base = base
        self.layer = layer
        self.tolerance = tolerance

        offset = 0

        for spec in specs:
            offset += self.__createGuardRing(offset, spec)

    def __createGuardRing(self, offset, spec):
        offset1 = gdspy.offset(self.base, offset + spec[0], join='round', tolerance=self.tolerance)
        offset2 = gdspy.offset(self.base, offset + spec[0] + spec[1], join='round', tolerance=self.tolerance)

        diff = gdspy.boolean(offset2, offset1, 'not', layer=self.layer)
        self.cell.add(diff)

        return spec[0] + spec[1]
