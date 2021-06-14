import gdspy
import math

from .Form import SimpleForm

class ChessBoard(SimpleForm):

    def __init__(self, layer, cell, size, N=(10, 10), inverted=False, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        self.size = size
        self.N = N
        self.inverted = inverted

        self.__createBoard()

    def __createBoard(self):
        nx = self.N[0]
        ny = self.N[1]
        s = self.size

        sx = nx*s
        sy = ny*s

        inv = self.inverted

        for xx in range(nx):
            x = -sx/2 + xx*s

            for yy in range(ny):
                y = -sy/2 + yy*s

                if (xx+yy)%2 == 0 ^ inv:
                    continue

                rect = gdspy.Rectangle((x-s/2, y-s/2), (x+s/2, y+s/2), **self.layer)

                self._add(rect)
