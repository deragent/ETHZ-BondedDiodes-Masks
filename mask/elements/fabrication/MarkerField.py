import gdspy

from .. import Element

from . import MarkerCoarse

class MarkerField(Element):

    def __init__(self, parent, name, config, arrowsize=20 layers=None, lib=None):

        self.config = config
        self.arrowsize = arrowsize

        super().__init__(parent, name, layers, lib)

    def construct(self):

        offset = 0

        for number, l1, l2, size in self.config:

            marker = MarkerCoarse(None, 'MARKER_%s_%s'%(l1, l2), number,
                l1, l2, size=size)
            self.cell.add(gdspy.CellReference(
                marker.cell,
                origin=(offset, 0)
            ))

            offset += marker.width*1.5

        self.__addArrows()
