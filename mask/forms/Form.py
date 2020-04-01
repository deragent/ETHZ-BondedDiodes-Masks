import gdspy

class SimpleForm():

    def __init__(self, layer, cell, origin=(0,0), angle=0, offset=0):

        self.offset = offset

        self.origin = origin
        self.angle = angle

        self.layer = layer
        self.cell = cell

    def _add(self, element):

        element = element.rotate(self.angle).translate(*self.origin)

        if self.offset != 0:
            self.cell.add(gdspay.offset(element, self.offset, join='miter', join_first=True, **self.layer))
        else:
            self.cell.add(element)
