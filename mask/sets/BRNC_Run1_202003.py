import gdspy
import math
import argparse

## Disable the default lib to make multi lib use possible
gdspy.library.use_current_library = False

from mask import config
from mask.processes import BRNC_202003
from mask.macros import Run1_TestSet

from mask.tools import MaskMerge

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine


parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-1 [202003].')
parser.add_argument('-o', '--output', required=True,
                    help='Name of the output file.')
parser.add_argument('-e', '--export', default=None,
                    help='Flag to export the fabrication mask layers into individual files.')

args = parser.parse_args()


### Create the library and top cell
lib = gdspy.GdsLibrary()
config.GLOBAL["LIB"] = lib

top = lib.new_cell('TOP_CELL')


### Create meta cells
wafer = Wafer(top, 'WAFER', 150000)
mask = Mask(top, 'MASK', 7*25400, {
        "DATE": "2020-03-12",
        "USER": "jorich",
        "LAYOUT": "DIODE-RUN-1"
    }, githash=True)


### Add Markers
markers, keepouts = BRNC_202003.createMarkers(lib)
top.add(markers)



### Create diode cells
diodes = lib.new_cell('DIODES')

d15 = Diode(None, 'DIODE_15mm', 15000)
d12 = Diode(None, 'DIODE_12mm', 12000)
d8 = Diode(None, 'DIODE_8mm', 8000)
d6 = Diode(None, 'DIODE_6mm', 6000)
d4 = Diode(None, 'DIODE_4mm', 4000)
d2 = Diode(None, 'DIODE_2mm', 2000)

margin = 150
dicingwidth = 100

xoffset = margin

ymin = [-61500, -61500, -57000, -51000, -45000, -40500]
ymax = 50300

for ii, d in enumerate([d15, d12, d8, d6, d4, d2]):

    x = xoffset + d.width/2

    column_r = DeviceColumn(diodes, 'COLUMN_R_%s'%(d.name), d.cell,
        x, ymin[ii], min(-1*ymin[ii], ymax),
        margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

    column_l = DeviceColumn(diodes, 'COLUMN_L_%s'%(d.name), d.cell,
        -1*x, ymin[ii], min(-1*ymin[ii], ymax),
        margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

    xoffset += d.width + 2*margin

top_dicing = DicingLine(config.GLOBAL["LAYERS"]["DICING"], diodes,
    dicingwidth, (-49000, 50000), (49000, 50000))

top.add(diodes)

## Add test structures (VPD + TLM)
testset = Run1_TestSet(lib)

top.add(gdspy.CellReference(testset, rotation=90, origin=(-61500, 0)))
top.add(gdspy.CellReference(testset, rotation=-90, origin=(+61500, 0)))
top.add(gdspy.CellReference(testset, rotation=0, origin=(0, +61500)))


### Save the gds file
lib.write_gds(args.output)
### Save and svg representation
top.write_svg(args.output + '.svg', 0.1)

if args.export is not None:
    merge = MaskMerge(top)

    for name, layers in config.GLOBAL["EXPORT"]:

        mask.setMaskName(name)

        merge.refresh()
        out = merge.mergeLayersIntoLib(layers, **config.GLOBAL["LAYERS"][name])

        out.write_gds(args.export + "/%s.gds"%(name))
