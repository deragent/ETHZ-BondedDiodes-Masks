import gdspy
import math

from .. import Element

from ...forms import Wheel
from ...forms import Stripes
from ...forms import ChessBoard

class Resolution(Element):

    def __init__(self, parent, name,
        layer,
        critical_dimension=5,
        layers=None, lib=None):

        self.critical_dimension = critical_dimension

        self.layer = layer

        super().__init__(parent, name, layers, lib)

    def construct(self):
        l = self.layers[self.layer]

        cd = self.critical_dimension

        cw = cd*150
        tw = 2*cw + 20*cd

        # Add Wheel
        wheel = Wheel(
            l, self.cell,
            cw/2, 20, radius_i=cd/10,
            origin=(-tw/2 + cw/2, -tw/2 + cw/2)
        )


        # Add N-times Chess Board
        mult = 1
        for x in [cw/4, 3*cw/4]:
            for y in [cw/4, 3*cw/4]:
                size = mult*cd
                N = math.floor(cw/3 / size)

                chess = ChessBoard(
                    l, self.cell,
                    size, N=(N, N),
                    origin=(tw/2 - x, tw/2 - y)
                )

                mult *= 2


        # Add stripes
        stripes = [cd*n/5 for n in range(1, 11)]
        N = 8

        maxw = (2*N-1)*max(stripes)

        x = -tw/2
        y = tw/2 - cw/4
        for ww, width in enumerate(stripes):

            x+= N*width


            strip = Stripes(
                l, self.cell,
                height=cw/3, strip=width, N=N,
                origin=(x, y)
            )

            # Add vertical stripes
            strip = Stripes(
                l, self.cell,
                height=cw/3, strip=width, N=N,
                origin=(y, x), angle=math.pi/2
            )

            # Add Horizontal stripes
            x += N*width + cd*15
            if x>=-20*cd:
                x = -tw/2
                y = tw/2 - 3*cw/4
