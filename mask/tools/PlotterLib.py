import gdspy

import re
import numpy as np

from .PlotterGenerator import PlotterGenerator
from .LibIterator import LibIterator, Transform

class PlotterLib(PlotterGenerator, LibIterator):

    def __init__(self, name, lib):

        PlotterGenerator.__init__(self, name)
        LibIterator.__init__(self, lib)

    def _transformBBox(self, t, bbox):
        result = np.zeros((2, 2))

        # Transform each corner point of the bounding box
        for pp, point in enumerate(list(bbox)):
            result[pp, :] = Transform.apply(t, point)

        return result

    def _exec(self, name, cell, t):
        # For each visited cell we add the transformed bbox
        self.addBBox(name, self._transformBBox(t, cell.get_bounding_box()))

    def generate(self):
        self.traverseAll()

        return PlotterGenerator.generate(self)
