import gdspy

import math

from mask import config

from mask.processes import BRNC_202003

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.test import Resistance, VanDerPauwMetal
from mask.elements.fabrication import MarkerCoarse

lib = gdspy.GdsLibrary()#infile='Nanoscribe_Wafer_25mmx25mm_WithMarkers2.gds')
config.GLOBAL["LIB"] = lib

top = lib.new_cell('TOP_CELL')

#top.add(lib.cells['noname'])

### Create meta cells

w = Wafer(top, 'WAFER', 150000)
m = Mask(top, 'MASK', 7*25400, {
        "DATE": "2020-03-12",
        "USER": "jorich",
        "LAYOUT": "DIODE-RUN-1"
    }, githash=True)


### Create diode cells

d15 = Diode(None, 'DIODE_15mm', 15000)
d12 = Diode(None, 'DIODE_12mm', 12000)
d8 = Diode(None, 'DIODE_8mm', 8000)
d6 = Diode(None, 'DIODE_6mm', 6000)
d4 = Diode(None, 'DIODE_4mm', 4000)
d2 = Diode(None, 'DIODE_2mm', 2000)

spacing = 1000

offset = spacing/2

ystart = [-53500, -55000, -50500, -45000, -38500, -33500]

for ii, d in enumerate([d15, d12, d8, d6, d4, d2]):

    yspacing = d.height + spacing

    xstart = offset + d.width/2

    n = math.ceil(-2*ystart[ii] / yspacing)
    if ii <= 2:
        n -= 1

    if ii == 2:
        n2 = math.ceil(-1*ystart[ii] / yspacing)

        yoffset = ystart[ii]+(n2+1)*yspacing

        top.add(gdspy.CellArray(d.cell, 1, n - n2 -1, (0, yspacing), origin=(xstart, yoffset)))
        top.add(gdspy.CellArray(d.cell, 1, n - n2 -1, (0, yspacing), origin=(-xstart, yoffset)))

        n = n2

    top.add(gdspy.CellArray(d.cell, 1, n, (0, yspacing), origin=(xstart, ystart[ii])))
    top.add(gdspy.CellArray(d.cell, 1, n, (0, yspacing), origin=(-xstart, ystart[ii])))

    offset += d.width + spacing


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
# vdp = VanDerPauwMetal(top, 'VDP_3mm', 1500)



### Add Markers
top.add(BRNC_202003.createMarkers(lib))


### Save the gds file

lib.write_gds('BRNC_Run1_202003.gds')

# gdspy.LayoutViewer(lib)
