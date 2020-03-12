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

        self.cell = self.lib.new_cell(name)

        self.construct()

        self._finalize()

    def construct(self):
        raise NotImplementedError()

    def _finalize(self):

        bbox = self.cell.get_bounding_box()

        self.width = bbox[1,0] - bbox[0,0]
        self.height = bbox[1,1] - bbox[0,1]

        if self.parent is not None:
            self.parent.add(self.cell)
