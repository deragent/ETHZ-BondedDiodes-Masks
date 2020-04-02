import gdspy
import math
import argparse

from mask import config
from mask.processes import BRNC_202003

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.test import Resistance, VanDerPauwMetal, VanDerPauwContact
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine


parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-1 [202003].')
parser.add_argument('-o', '--output', required=True,
                    help='Name of the output file.')

args = parser.parse_args()


### Create the library and top cell
lib = gdspy.GdsLibrary()
config.GLOBAL["LIB"] = lib

top = lib.new_cell('TOP_CELL')


### Create meta cells
w = Wafer(top, 'WAFER', 150000)
m = Mask(top, 'MASK', 7*25400, {
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



### Add resistive test structures
testres = lib.new_cell('TEST_RES')

r5 = Resistance(None, 'RES_5mm', 5000)
r10 = Resistance(None, 'RES_10mm', 10000)
r15 = Resistance(None, 'RES_15mm', 15000)
r20 = Resistance(None, 'RES_20mm', 20000)


testres.add(gdspy.CellReference(r15.cell, origin=(-1.1*r15.width, 0)))
testres.add(gdspy.CellReference(r15.cell, origin=(0*r15.width, 0)))
testres.add(gdspy.CellReference(r15.cell, origin=(+1.1*r15.width, 0)))

testres.add(gdspy.CellReference(r20.cell, origin=(-0.55*r20.width, 1.5*r15.height)))
testres.add(gdspy.CellReference(r20.cell, origin=(0.55*r20.width, 1.5*r15.height)))

testres.add(gdspy.CellReference(r10.cell, origin=(-1.1*r10.width, 3*r15.height)))
testres.add(gdspy.CellReference(r10.cell, origin=(0*r10.width, 3*r15.height)))
testres.add(gdspy.CellReference(r10.cell, origin=(+1.1*r10.width, 3*r15.height)))

testres.add(gdspy.CellReference(r5.cell, origin=(-1.1*r5.width, 4.5*r15.height)))
testres.add(gdspy.CellReference(r5.cell, origin=(0*r5.width, 4.5*r15.height)))
testres.add(gdspy.CellReference(r5.cell, origin=(+1.1*r5.width, 4.5*r15.height)))

top.add(gdspy.CellReference(testres, rotation=90, origin=(-62000, 0)))
top.add(gdspy.CellReference(testres, rotation=-90, origin=(+62000, 0)))
top.add(gdspy.CellReference(testres, rotation=0, origin=(0, +62000)))



### Add VDP test structures
# vdp = VanDerPauwMetal(top, 'VDP_3mm', contactw=1000, contactspacing=2540)
# vdp = VanDerPauwContact(top, 'VDP_3mm', contactw=1000, contactspacing=2540)



### Save the gds file
lib.write_gds(args.output)
