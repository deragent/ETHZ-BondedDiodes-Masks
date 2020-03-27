import gdspy

from .. import config

from ..elements.fabrication import MarkerField

## Define the layers

config.GLOBAL["LAYERS"]["WAFER_OUTLINE"] = (52, 1)

config.GLOBAL["LAYERS"]["MASK_OUTLINE"] = (61, 2)

config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"] = (11, 0)
config.GLOBAL["LAYERS"]["CONTACT_DOPING"] = (12, 0)
config.GLOBAL["LAYERS"]["METALIZATION"] = (13, 0)
config.GLOBAL["LAYERS"]["PASSIVATION_OPEN"] = (14, 0)


config.GLOBAL["LAYERS"]["MASK_LABEL"] =(62, 3)


## Create the marker layout
def createMarkers(lib):

    markers = lib.new_cell('MARKERS')

    field = MarkerField(None, 'MARKER_FIELD', [
        ('1', 'ALIGNMENT_MARKS', 'CONTACT_DOPING', 20),
        ('2', 'ALIGNMENT_MARKS', 'METALIZATION', 20),
    ])

    markers.add(gdspy.CellReference(field.cell, origin=(-35000, 0)))
    markers.add(gdspy.CellReference(field.cell, origin=(+35000, 0)))

    return markers
