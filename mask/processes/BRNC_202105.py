import gdspy
import math

from .. import config

from ..elements.fabrication import MarkerField
from ..forms import ScaleBarVertical
from ..elements.fabrication import WaferFlatAligner
from ..forms import Ring

## Define the layers

config.GLOBAL["LAYERS"]["WAFER_BORDER"] = (51, 1)
config.GLOBAL["LAYERS"]["WAFER_OUTLINE"] = (52, 1)

config.GLOBAL["LAYERS"]["DICING"] = (53, 4)

config.GLOBAL["LAYERS"]["MASK_CORNERS"] = (60, 2)
config.GLOBAL["LAYERS"]["MASK_OUTLINE"] = (61, 2)

# Only one etching step for alignment and isolation trench
config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"] = (11, 0)
config.GLOBAL["LAYERS"]["CONTACT_DOPING"] = (12, 0)
config.GLOBAL["LAYERS"]["METALIZATION"] = (13, 0)
config.GLOBAL["LAYERS"]["PASSIVATION_OPEN"] = (14, 0)
config.GLOBAL["LAYERS"]["ISOLATION_TRENCH"] = (15, 0)

config.GLOBAL["LAYERS"]["MASK_LABEL"] =(62, 3)
config.GLOBAL["LAYERS"]["MASK_NAME"] =(63, 3)

config.GLOBAL["LAYERS"]["EXPORT_ALIGNMENT_MARKS"] = (111, 0)
config.GLOBAL["LAYERS"]["EXPORT_CONTACT_DOPING"] = (112, 0)
config.GLOBAL["LAYERS"]["EXPORT_METALIZATION"] = (113, 0)
config.GLOBAL["LAYERS"]["EXPORT_PASSIVATION_OPEN"] = (114, 0)
config.GLOBAL["LAYERS"]["EXPORT_DICING"] = (115, 0)
config.GLOBAL["LAYERS"]["EXPORT_TRENCH"] = (116, 0)



## Define the export specifications

config.GLOBAL["EXPORT"].add("EXPORT_ALIGNMENT_MARKS", config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"])
config.GLOBAL["EXPORT"].add("EXPORT_CONTACT_DOPING", config.GLOBAL["LAYERS"]["CONTACT_DOPING"])
config.GLOBAL["EXPORT"].add("EXPORT_METALIZATION", config.GLOBAL["LAYERS"]["METALIZATION"])
config.GLOBAL["EXPORT"].add("EXPORT_PASSIVATION_OPEN", config.GLOBAL["LAYERS"]["PASSIVATION_OPEN"])
config.GLOBAL["EXPORT"].add("EXPORT_DICING", config.GLOBAL["LAYERS"]["DICING"])
config.GLOBAL["EXPORT"].add("EXPORT_DICING", config.GLOBAL["LAYERS"]["WAFER_BORDER"])
config.GLOBAL["EXPORT"].add("EXPORT_TRENCH", config.GLOBAL["LAYERS"]["ISOLATION_TRENCH"])

config.GLOBAL["EXPORT"].always(config.GLOBAL["LAYERS"]["MASK_LABEL"])
config.GLOBAL["EXPORT"].always(config.GLOBAL["LAYERS"]["MASK_NAME"])


## Create the marker layout
def createMarkers(lib):

    markers = lib.new_cell('MARKERS')

    # The positions are hard-coded here, as the alignment mark mask has been
    # written before finalizing the design. As the METALIZATION and
    # ISOLATION_TRENCH marks have to be inverted, this lead to a shift in the
    # location of the alignment marks!
    field = MarkerField(lib, 'MARKER_FIELD', [
        ('1', 'ALIGNMENT_MARKS', 'CONTACT_DOPING', 20, False, True),
        ('2', 'ALIGNMENT_MARKS', 'METALIZATION', 20, False, True),
        ('3', 'ALIGNMENT_MARKS', 'ISOLATION_TRENCH', 20, False, True),
    ], position=[0, 1640, 1640+1620])


    marker_left = gdspy.CellReference(field.cell, origin=(-42000, 0))
    markers.add(marker_left)

    marker_right = gdspy.CellReference(field.cell, origin=(+42000, 0), x_reflection=True, rotation=180)
    markers.add(marker_right)

    keepouts = [marker_left.get_bounding_box(), marker_right.get_bounding_box()]

    return markers, keepouts


def createWaferAlignment(lib):

    layer = config.GLOBAL["LAYERS"]["ALIGNMENT_MARKS"]

    markers = lib.new_cell('WAFER_MARKERS')

    RADIUS = 100000/2


    # Create the outline ring
    temp_cell = lib.new_cell('TEMP_CELL')
    outline = Ring(layer, temp_cell, RADIUS - 3000, RADIUS + 3000, flat=35000)

    polygons = temp_cell.get_polygons()
    lib.remove(temp_cell)


    # Add side markers
    ## Angle of 110° is chosen, so that marks still lie within field of MA6
    for angle in [+60, -60, +110, -110]:
        x = math.sin(angle/180*math.pi)*RADIUS
        y = -math.cos(angle/180*math.pi)*RADIUS

        temp_cell = lib.new_cell('TEMP_CELL')

        marker = ScaleBarVertical(
            layer, temp_cell, left=angle<0,
            height=500, step=50,
            origin=(x, y), angle=angle/180*math.pi)

        polygons = gdspy.boolean(polygons, temp_cell.get_polygons(), 'not', **layer)

        lib.remove(temp_cell)


    # Add flat markers
    marker_flat = WaferFlatAligner(
        None, 'WAFER_MARKER_FLAT', RADIUS*2, 32500, 'ALIGNMENT_MARKS', height=1500
    )
    polygons = gdspy.boolean(polygons, marker_flat.cell.get_polygons(), 'not', **layer)

    markers.add(polygons)

    return markers
