import gdspy

class MaskMerge():

    def __init__(self, cell):

        self.cell = cell

        self.refresh()

    def refresh(self):
        self.polygons = self.cell.get_polygons(by_spec=True)

    def mergeLayersIntoLib(self, mergelayers, layer, datatype):

        lib = gdspy.GdsLibrary()
        top = lib.new_cell('TOP_CELL')

        self.mergeLayers(mergelayers, top, layer, datatype)

        return lib

    def mergeLayers(self, mergelayers, cell, layer, datatype):

        polygons = []

        for pLayer, pDatatype in self.polygons:
            ## Currently matching is only done base on layer and not datatype
            if pLayer not in mergelayers:
                continue

            polygons.extend(self.polygons[(pLayer, pDatatype)])

        set = gdspy.PolygonSet(polygons)
        set = gdspy.boolean(set, None, 'or', layer=layer, datatype=datatype)

        cell.add(set)
