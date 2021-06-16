import gdspy

from .. import config

class Element():

    def __init__(self, parent, name, layers=None, lib=None):

        self.parent = parent
        self.name = name

        if layers is None:
            layers = config.GLOBAL["LAYERS"]
        self.layers = layers

        if lib is None:
            lib = config.GLOBAL["LIB"]
        self.lib = lib

        self.cell = gdspy.Cell(name)

        self.construct()

        self._finalize()

    def construct(self):
        raise NotImplementedError()

    def addBBoxDicing(self, width, margin, layer, bbox = None):

        if bbox is None:
            bbox = self.cell.get_bounding_box()
        if bbox is None:
            return

        outer = gdspy.Rectangle(bbox[0] - margin - width/2, bbox[1] + margin + width/2, **self.layers["DICING"])
        inner = gdspy.Rectangle(bbox[0] - margin + width/2, bbox[1] + margin - width/2, **self.layers["DICING"])

        dicing = gdspy.boolean(outer, inner, 'not', **self.layers["DICING"])

        self.cell.add(dicing)

    def _finalize(self):

        bbox = self.cell.get_bounding_box()

        self.width = bbox[1,0] - bbox[0,0]
        self.height = bbox[1,1] - bbox[0,1]

        if self.parent is not None:
            self.parent.add(self.cell)
