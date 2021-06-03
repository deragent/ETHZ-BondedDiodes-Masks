import gdspy
import math

from .. import Element

class CTLMContact(Element):

    def __init__(self, parent, name,
        gaps, grid,
        radius_i=100, size=400,
        with_contact_implant=True,
        layers=None, lib=None):

        self.gaps = gaps
        self.gaps.sort()

        self.grid = grid
        if self.grid[0]*self.grid[1] < len(self.gaps):
            print("[Warning] Number of gaps [%i] is larger than grid space [%i x %i = %i]!"%(
                len(self.gaps), self.grid[0], self.grid[1], self.grid[1]*self.grid[0]))

        self.radius_i = radius_i
        self.size = size

        self.with_contact_implant = with_contact_implant

        super().__init__(parent, name, layers, lib)


    def construct(self):
        s = self.size
        ri = self.radius_i

        gx = self.grid[0]
        gy = self.grid[1]
        gt = gx*gy

        th = s*(2*gy)
        tw = s*(2*gx + 1)


        if self.with_contact_implant:
            implant = gdspy.Rectangle((-tw/2, -th/2), (tw/2, th/2), **self.layers["CONTACT_DOPING"])
            self.cell.add(implant)

        metal = gdspy.Rectangle((-tw/2, -th/2), (tw/2, th/2), **self.layers["METALIZATION"])


        x_start = -tw/2 + s
        x = x_start
        y = -th/2 + s

        for gg, gap in enumerate(self.gaps):

            outer = gdspy.Round((x, y), ri + gap, **self.layers["METALIZATION"])
            metal = gdspy.boolean(metal, outer, 'not', **self.layers["METALIZATION"])

            inner = gdspy.Round((x, y), ri, **self.layers["METALIZATION"])
            metal = gdspy.boolean(metal, inner, 'or', **self.layers["METALIZATION"])

            if gg+1 >= gt:
                # Reached maximum grid size
                break

            if ((gg + 1)%gx) == 0:
                y += 2*s
                x = x_start
            else:
                x += 2*s

        self.cell.add(metal)
