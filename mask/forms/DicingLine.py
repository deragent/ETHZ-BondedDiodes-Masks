import gdspy
import math

class DicingLine():

    def __init__(self, layer, cell, width, p1, p2):

        self.cell = cell
        self.layer = layer

        self.width = width
        self.p = [p1, p2]
        self.__createLine()

    def __createLine(self):

        path = gdspy.FlexPath(self.p, self.width, **self.layer)

        self.cell.add(path)
