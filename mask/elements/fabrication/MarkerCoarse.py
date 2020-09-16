import gdspy
import math

from .. import Element

class MarkerCoarse(Element):

    def __init__(self, parent, name, number, layer1, layer2, size=20, inverted=(False, False), layers=None, lib=None):

        self.number = number

        self.layer1 = layer1
        self.layer2 = layer2

        self.size = size

        self.inverted = inverted

        self._elements = ( [] , [] )

        super().__init__(parent, name, layers, lib)

    def __addToLayer1(self, element):
        self._elements[0].append(element)

    def __addToLayer2(self, element):
        self._elements[1].append(element)

    def drawElements(self):

        data = zip(
                self._elements,
                (self.layers[self.layer1], self.layers[self.layer2]),
                self.inverted
        )

        for elements, layer, inverted in data:

            if inverted:
                s = self.size
                base = gdspy.Rectangle((-41*s, -41*s), (41*s, 41*s), **layer)

                for element in elements:
                    base = gdspy.boolean(base, element, 'not', **layer)

                self.cell.add(base)

            else:
                for element in elements:
                    self.cell.add(element)

    def construct(self):

        l1 = self.layers[self.layer1]
        l2 = self.layers[self.layer2]

        s = self.size

        ## Outer Border
        outer = gdspy.Rectangle((-20*s, -20*s), (20*s, 20*s))
        inner = gdspy.Rectangle((-17*s, -17*s), (17*s, 17*s))

        border = gdspy.boolean(outer, inner, 'not', **l1)
        self.__addToLayer1(border)

        ## Anti-Cross
        rect = gdspy.Rectangle((-15*s, -15*s), (-4*s, -4*s), **l1)
        for xx in [0, 1]:
            for yy in [0, 1]:
                rect_offset = gdspy.copy(rect, xx*19*s, yy*19*s)

                if xx == 0 and yy==1:
                    number = gdspy.Text(self.number, 9*s, (-12*s, 4*s), **l2)
                    self.__addToLayer2(number)

                    self.__addToLayer1(gdspy.boolean(rect_offset, gdspy.copy(number), 'not', **l1))
                else:
                    self.__addToLayer1(rect_offset)

        ## Cross
        hori = gdspy.Rectangle((-15*s, -2*s), (15*s, 2*s))
        vert = gdspy.Rectangle((-2*s, -15*s), (2*s, 15*s))

        self.__addToLayer2(gdspy.boolean(hori, vert, 'or', **l2))

        ## "Hairs"
        for angle in [0, math.pi/2, math.pi, math.pi*3/2]:
            self.__createHairBar(22*s, 12*s, angle)
            self.__createHairBar(22*s, -12*s, angle)

        self.drawElements()

    def __createHairBar(self, x, y, rotation):

        l1 = self.layers[self.layer1]
        l2 = self.layers[self.layer2]

        s = self.size

        base1 = gdspy.Rectangle((x+2*s, y-s/2), (x+5*s, y+s/2), **l1)
        base2 = gdspy.Rectangle((x, y-s/2), (x+3*s, y+s/2), **l2)

        for ii in [-4, -3, -2, -1, 1, 2, 3, 4]:
            base1 = gdspy.boolean(base1, gdspy.Rectangle((x+2*s, y-s/2+ii*2*s*1.05), (x+5*s, y+s/2+ii*2*s*1.05)), 'or', **l1)
            base2 = gdspy.boolean(base2, gdspy.Rectangle((x, y-s/2+ii*2*s), (x+3*s, y+s/2+ii*2*s)), 'or', **l2)


        self.__addToLayer1(base1.rotate(rotation))
        self.__addToLayer2(base2.rotate(rotation))
