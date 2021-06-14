import gdspy

from .Form import SimpleForm

class Stripes(SimpleForm):

    def __init__(self, layer, cell, height, strip, N, origin=(0,0), angle=0, offset=0):

        super().__init__(layer, cell, origin, angle, offset)

        width = (2*N - 1)*strip

        x = -width/2
        for nn in range(N):
            self._add(gdspy.Rectangle((x, -height/2), (x+strip, height/2), **self.layer))

            x += 2*strip
