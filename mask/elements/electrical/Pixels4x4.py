import gdspy
import math

from .. import Element

class Pixels4x4(Element):

    def __init__(self, parent, name,
        size, implantsize,
        contactsize=400, trench=50, overhang=10,
        back=False, margin=150, dicingwidth=100,
        layers=None, lib=None):

        self.size = size
        self.implantsize = implantsize
        self.contactsize = contactsize
        self.trench = trench

        self.overhang = overhang
        self.margin = margin
        self.dicingwidth = dicingwidth

        self.back = back

        super().__init__(parent, name, layers, lib)

    def construct(self):

        t = self.trench
        s = self.size
        c = self.contactsize
        d = self.dicingwidth
        oh = self.overhang

        w = self.contactsize/10

        ts = 2*t + 2*w  # Trench separation

        tw = 4*s + (4+1)*ts

        if not self.back:
            # Add all pixels
            y = -tw/2 + ts + s/2

            for yy in range(4):
                x = -tw/2 + ts + s/2

                for xx in range(4):
                    inner = False
                    if yy == 0:
                        orientation = math.pi
                    elif yy == 3:
                        orientation = 0
                    elif xx == 0:
                        orientation = math.pi/2
                    elif xx == 3:
                        orientation = -math.pi/2
                    else:
                        inner = True

                    if not inner:
                        self.__createOuterPixel(x, y, orientation)
                    else:
                        self.__createInnerPixel(x, y, left=xx<2, up=yy<2)

                    x += s + ts

                y += s + ts


        else:
            self.cell.add(gdspy.Rectangle(
                (-tw/2, -tw/2), (tw/2, tw/2),
                **self.layers["CONTACT_DOPING"]
            ))
            self.cell.add(gdspy.Rectangle(
                (-tw/2+oh, -tw/2+oh), (tw/2-oh, tw/2-oh),
                **self.layers["METALIZATION"]
            ))

        dw = tw + 2.5*c
        self.addBBoxDicing(
            self.dicingwidth, self.margin, "DICING",
            [[-dw/2, -dw/2], [dw/2, dw/2]]
        )


    def __createInnerPixel(self, x, y, left=True, up=True):

        s = self.size
        i = self.implantsize
        c = self.contactsize
        t = self.trench
        oh = self.overhang

        w = self.contactsize/10

        ts = 2*t + 2*w  # Trench separation
        ds = s+ts


        # Define contact implant
        implant = gdspy.Rectangle((x-i/2, y-i/2), (x+i/2, y+i/2), **self.layers["CONTACT_DOPING"])
        self.cell.add(implant)


        # Define the metal
        cd = s + c/2 ## Contact distance

        via = gdspy.Rectangle((x-i/2+oh, y-i/2+oh), (x+i/2-oh, y+i/2-oh), **self.layers["METALIZATION"])

        wire = gdspy.Path(w, (x, y))
        wire.segment(math.sqrt(2)*(s/2+t+w), -3/4*math.pi, **self.layers["METALIZATION"])
        wire.turn(0, -1/4*math.pi, **self.layers["METALIZATION"])
        wire.segment(s + 4*t, **self.layers["METALIZATION"])
        wire.turn(0, +1/4*math.pi, **self.layers["METALIZATION"])
        wire.segment(math.sqrt(2)*(c/2), **self.layers["METALIZATION"])

        contact = gdspy.Rectangle((x-cd-ds-c/2, y-ds-c/2), (x-cd-ds+c/2, y-ds+c/2), **self.layers["METALIZATION"]);

        metal = gdspy.boolean(via, wire, 'or', **self.layers["METALIZATION"])
        metal = gdspy.boolean(metal, contact, 'or', **self.layers["METALIZATION"])

        if not left:
            metal.mirror((x, y-10), (x, y+10))
        if not up:
            metal.mirror((x-10, y), (x+10, y))
        self.cell.add(metal)


        # Define the trench etch
        outer = gdspy.Rectangle((x-s/2-t, y-s/2-t), (x+s/2+t, y+s/2+t), **self.layers["ISOLATION_TRENCH"])
        inner = gdspy.Rectangle((x-s/2, y-s/2), (x+s/2, y+s/2), **self.layers["ISOLATION_TRENCH"])
        wirepass = gdspy.Path(2*w, (x, y))
        wirepass.segment(math.sqrt(2)*(s/2+t+w), -3/4*math.pi, **self.layers["ISOLATION_TRENCH"])

        trench = gdspy.boolean(outer, inner, 'not', **self.layers["ISOLATION_TRENCH"])
        trench = gdspy.boolean(trench, wirepass, 'not', **self.layers["ISOLATION_TRENCH"])

        if not left:
            trench.mirror((x, y-10), (x, y+10))
        if not up:
            trench.mirror((x-10, y), (x+10, y))
        self.cell.add(trench)



    def __createOuterPixel(self, x, y, orientation=0):

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

        if orientation != 0:
            metal.rotate(orientation, center=(x, y))
        self.cell.add(metal)


        # Define the trench etch
        outer = gdspy.Rectangle((x-s/2-t, y-s/2-t), (x+s/2+t, y+s/2+t), **self.layers["ISOLATION_TRENCH"])
        inner = gdspy.Rectangle((x-s/2, y-s/2), (x+s/2, y+s/2), **self.layers["ISOLATION_TRENCH"])
        wirepass = gdspy.Rectangle((x-w, y-w/2), (x+w, y+cd+w/2), **self.layers["ISOLATION_TRENCH"])

        trench = gdspy.boolean(outer, inner, 'not', **self.layers["ISOLATION_TRENCH"])
        trench = gdspy.boolean(trench, wirepass, 'not', **self.layers["ISOLATION_TRENCH"])

        if orientation != 0:
            trench.rotate(orientation, center=(x, y))
        self.cell.add(trench)
