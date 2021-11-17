import numpy as np

CLASS_TEMPLATE = """import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

class BBoxElement():

    def __init__(self, id, bbox):
        self.id = id
        self.bbox = np.array(bbox)

    def path(self):
        codes = [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
        vertices = [bbox[0,:], (bbox[0,0], bbox[1,1]), bbox[1,:], (bbox[1,0], bbox[0,1]), (0,0)]

        return Path(vertices, codes)

class %s():

    ELEMENTS = {
%s
    }

    def __init__(self, ax):
        self.ax = ax

    def plot(self, dev, **kwargs):
        patch = PathPatch(self.ELEMENTS[dev].path(), **kwargs)

        self.ax.add_patch(patch)
"""

BBOX_TEMPLATE = "\"%s\": BBoxElement(\"%s\", %s)"


class PlotterGenerator():

    BBOX = 1
    POLYGONS = 2

    def __init__(self, name):

        self.name = name
        self.elements = {}

        self.code = None

    def addBBox(self, id, bbox):
        self.elements[id] = (self.BBOX, bbox)

    def addPolygons(self, id, polygons):
        self.elements[id] = (self.POLYGONS, polygons)

    def remove(self, id):
        del self.elements[id]

    def print(self):
        print(self)

    def write(self, file):
        with open(file, 'w') as f:
            f.write(str(self))

    def __str__(self):
        if self.code is None:
            self.generate()

        return self.code


    def generateBBox(self, id, data):

        return BBOX_TEMPLATE%(id, id, np.array2string(data, separator=', ').replace('\n', ' '))


    def generate(self):

        elements = []

        for id, data in self.elements.items():
            type, data = data

            if type == self.BBOX:
                elements.append(self.generateBBox(id, data))
            else:
                # TODO Implement Polygons Generator
                raise Exception("Type [%i] not implemented yet!"%(type))

        self.code = CLASS_TEMPLATE%(self.name, ",\n".join([" "*8 + e for e in elements]))
