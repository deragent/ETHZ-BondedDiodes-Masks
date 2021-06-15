import gdspy
import math

from .. import Element

class Pixels2xN(Element):

    def __init__(self, parent, name,
        N, size, implantsize,
        contactsize=400, trench=50, overhang=10,
        dicingwidth=100,
        layers=None, lib=None):

        self.N = N
        self.size = size
        self.implantsize = implantsize
        self.contactsize = contactsize
        self.trench = trench

        self.overhang = overhang
        self.dicingwidth = dicingwidth

        super().__init__(parent, name, layers, lib)

    def construct(self):

        t = self.trench
        s = self.size
        c = self.contactsize
        N = self.N
        d = self.dicingwidth

        tw = N*s + (N+1)*t
        th = 2*(s*1.5+c) + d

        # Add all pixels
        x = -tw/2 + t + s/2
        for nn in range(N):
            self.__createPixel(x, (s+t)/2, True)
            self.__createPixel(x, -(s+t)/2, False)

            x += s + t


        # Define the dicing lines
        outer = gdspy.Rectangle((-tw/2 - 3*d, -th/2 - 3*d), (tw/2 + 3*d, th/2 + 3*d), **self.layers["DICING"])
        inner = gdspy.Rectangle((-tw/2 - 2*d, -th/2 - 2*d), (tw/2 + 2*d, th/2 + 2*d), **self.layers["DICING"])

        dicing = gdspy.boolean(outer, inner, 'not', **self.layers["DICING"])

        self.cell.add(dicing)


    def __createPixel(self, x, y, up=True):

        s = self.size
        i = self.implantsize
        c = self.contactsize
        t = self.trench
        oh = self.overhang

        w = self.contactsize/10

        # Define contact implant
        implant = gdspy.Rectangle((x-i/2, y-i/2), (x+i/2, y+i/2), **self.layers["CONTACT_DOPING"])
        self.cell.add(implant)


        # Define the metal
        cd = s + c/2 ## Contact distance

        via = gdspy.Rectangle((x-i/2+oh, y-i/2+oh), (x+i/2-oh, y+i/2-oh), **self.layers["METALIZATION"])
        wire = gdspy.Rectangle((x-w/2, y-w/2), (x+w/2, y+cd+w/2), **self.layers["METALIZATION"])
        contact = gdspy.Rectangle((x-c/2, y+cd-c/2), (x+c/2, y+cd+c/2), **self.layers["METALIZATION"]);

        metal = gdspy.boolean(via, wire, 'or', **self.layers["METALIZATION"])
        metal = gdspy.boolean(metal, contact, 'or', **self.layers["METALIZATION"])

        if not up:
            metal.rotate(math.pi, center=(x, y))
        self.cell.add(metal)


        # Define the trench etch
        outer = gdspy.Rectangle((x-s/2-t, y-s/2-t), (x+s/2+t, y+s/2+t), **self.layers["ISOLATION_TRENCH"])
        inner = gdspy.Rectangle((x-s/2, y-s/2), (x+s/2, y+s/2), **self.layers["ISOLATION_TRENCH"])
        wirepass = gdspy.Rectangle((x-w, y-w/2), (x+w, y+cd+w/2), **self.layers["METALIZATION"])

        trench = gdspy.boolean(outer, inner, 'not', **self.layers["ISOLATION_TRENCH"])
        trench = gdspy.boolean(trench, wirepass, 'not', **self.layers["ISOLATION_TRENCH"])

        if not up:
            trench.rotate(math.pi, center=(x, y))
        self.cell.add(trench)
