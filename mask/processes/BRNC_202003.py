import gdspy
import math

from .. import config

from ..elements.fabrication import MarkerField
from ..elements.fabrication import WaferAligner
from ..elements.fabrication import WaferFlatAligner
from ..forms import Ring

## Define the layers

config.GLOBAL["LAYERS"]["WAFER_OUTLINE"] = (52, 1)

config.GLOBAL["LAYERS"]["DICING"] = (53, 4)

config.GLOBAL["LAYERS"]["MASK_CORNERS"] = (60, 2)
config.GLOBAL["LAYERS"]["MASK_OUTLINE"] = (61, 2)

config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"] = (11, 0)
config.GLOBAL["LAYERS"]["CONTACT_DOPING"] = (12, 0)
config.GLOBAL["LAYERS"]["METALIZATION"] = (13, 0)
config.GLOBAL["LAYERS"]["PASSIVATION_OPEN"] = (14, 0)

config.GLOBAL["LAYERS"]["MASK_LABEL"] =(62, 3)
config.GLOBAL["LAYERS"]["MASK_NAME"] =(63, 3)

config.GLOBAL["LAYERS"]["EXPORT_ALIGNMENT_MARKS"] = (111, 0)
config.GLOBAL["LAYERS"]["EXPORT_CONTACT_DOPING"] = (112, 0)
config.GLOBAL["LAYERS"]["EXPORT_METALIZATION"] = (113, 0)
config.GLOBAL["LAYERS"]["EXPORT_PASSIVATION_OPEN"] = (114, 0)



## Define the export specifications

config.GLOBAL["EXPORT"].add("EXPORT_ALIGNMENT_MARKS", config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"])
config.GLOBAL["EXPORT"].add("EXPORT_CONTACT_DOPING", config.GLOBAL["LAYERS"]["CONTACT_DOPING"])
config.GLOBAL["EXPORT"].add("EXPORT_METALIZATION", config.GLOBAL["LAYERS"]["METALIZATION"])
config.GLOBAL["EXPORT"].add("EXPORT_METALIZATION", config.GLOBAL["LAYERS"]["MASK_CORNERS"]) # To properly write the dark field mask
config.GLOBAL["EXPORT"].add("EXPORT_PASSIVATION_OPEN", config.GLOBAL["LAYERS"]["PASSIVATION_OPEN"])

config.GLOBAL["EXPORT"].always(config.GLOBAL["LAYERS"]["MASK_LABEL"])
config.GLOBAL["EXPORT"].always(config.GLOBAL["LAYERS"]["MASK_NAME"])


## Create the marker layout
def createMarkers(lib):

    markers = lib.new_cell('MARKERS')

    field = MarkerField(lib, 'MARKER_FIELD', [
        ('1', 'ALIGNMENT_MARKS', 'CONTACT_DOPING', 20, False, True),
        ('2', 'ALIGNMENT_MARKS', 'METALIZATION', 20, False, False),
    ])


    marker_left = gdspy.CellReference(field.cell, origin=(-55000, 0))
    markers.add(marker_left)

    marker_right = gdspy.CellReference(field.cell, origin=(+55000, 0), x_reflection=True, rotation=180)
    markers.add(marker_right)

    keepouts = [marker_left.get_bounding_box(), marker_right.get_bounding_box()]

    return markers, keepouts


def createWaferAlignment(lib):

    layer = config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"]

    markers = lib.new_cell('WAFER_MARKERS')

    RADIUS = 150000/2

    outline_cell = lib.new_cell('WAFER_OUTLINE')
    outline = Ring(layer, outline_cell, RADIUS - 3000, RADIUS + 3000, flat=60000)

    polygons = outline_cell.get_polygons()

    # Top Markers
    y = 25000
    x = math.sqrt(RADIUS**2 - y**2)

    marker_tr = WaferAligner(None, 'WAFER_MARKER_TR', (x, y), 'ALIGNMENT_MARKS', inverted=False)
    marker_tl = WaferAligner(None, 'WAFER_MARKER_TL', (-x, y), 'ALIGNMENT_MARKS', inverted=False)

    polygons = gdspy.boolean(polygons, marker_tr.cell.get_polygons(), 'not', **layer)
    polygons = gdspy.boolean(polygons, marker_tl.cell.get_polygons(), 'not', **layer)

    # Bottom Markers
    y = RADIUS/2
    x = math.sqrt(RADIUS**2 - y**2)

    marker_br = WaferAligner(None, 'WAFER_MARKER_BR', (x, -y), 'ALIGNMENT_MARKS', inverted=False)
    marker_bl = WaferAligner(None, 'WAFER_MARKER_BL', (-x, -y), 'ALIGNMENT_MARKS', inverted=False)

    polygons = gdspy.boolean(polygons, marker_br.cell.get_polygons(), 'not', **layer)
    polygons = gdspy.boolean(polygons, marker_bl.cell.get_polygons(), 'not', **layer)

    marker_flat = WaferFlatAligner(
        None, 'WAFER_MARKER_FLAT', RADIUS*2, 57500, 'ALIGNMENT_MARKS',
        inverted=False
    )
    polygons = gdspy.boolean(polygons, marker_flat.cell.get_polygons(), 'not', **layer)

    markers.add(polygons)

    return markers
