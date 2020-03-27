import gdspy
import math

from .. import Element

class MarkerCoarse(Element):

    def __init__(self, parent, name, number, layer1, layer2, size=20, layers=None, lib=None):

        self.number = number

        self.layer1 = layer1
        self.layer2 = layer2

        self.size = size

        super().__init__(parent, name, layers, lib)

    def construct(self):

        l1 = self.layers[self.layer1]
        l2 = self.layers[self.layer2]

        s = self.size

        ## Outer Border
        outer = gdspy.Rectangle((-20*s, -20*s), (20*s, 20*s))
        inner = gdspy.Rectangle((-17*s, -17*s), (17*s, 17*s))

        border = gdspy.boolean(outer, inner, 'not', **l1)
        self.cell.add(border)

        ## Anti-Cross
        rect = gdspy.Rectangle((-15*s, -15*s), (-4*s, -4*s), **l1)
        for xx in [0, 1]:
            for yy in [0, 1]:
                rect_offset = gdspy.copy(rect, xx*19*s, yy*19*s)

                if xx == 0 and yy==1:
                    number = gdspy.Text(self.number, 9*s, (-12*s, 4*s), **l2)
                    self.cell.add(number)

                    self.cell.add(gdspy.boolean(rect_offset, gdspy.copy(number), 'not', **l1))
                else:
                    self.cell.add(rect_offset)

        ## Cross
        hori = gdspy.Rectangle((-15*s, -2*s), (15*s, 2*s))
        vert = gdspy.Rectangle((-2*s, -15*s), (2*s, 15*s))

        self.cell.add(gdspy.boolean(hori, vert, 'or', **l2))

        ## "Hairs"
        for angle in [0, math.pi/2, math.pi, math.pi*3/2]:
            self.__createHairBar(22*s, 12*s, angle)
            self.__createHairBar(22*s, -12*s, angle)


    def __createHairBar(self, x, y, rotation):

        l1 = self.layers[self.layer1]
        l2 = self.layers[self.layer2]

        s = self.size

        base1 = gdspy.Rectangle((x+2*s, y-s/2), (x+5*s, y+s/2), **l1)
        base2 = gdspy.Rectangle((x, y-s/2), (x+3*s, y+s/2), **l2)

        for ii in [-4, -3, -2, -1, 1, 2, 3, 4]:
            base1 = gdspy.boolean(base1, gdspy.Rectangle((x+2*s, y-s/2+ii*2*s*1.05), (x+5*s, y+s/2+ii*2*s*1.05)), 'or', **l1)
            base2 = gdspy.boolean(base2, gdspy.Rectangle((x, y-s/2+ii*2*s), (x+3*s, y+s/2+ii*2*s)), 'or', **l2)


        self.cell.add(base1.rotate(rotation))
        self.cell.add(base2.rotate(rotation))
