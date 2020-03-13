import gdspy

import math

from mask import config

from mask.processes import BRNC_202003

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask

lib = gdspy.GdsLibrary()
config.GLOBAL["LIB"] = lib

top = lib.new_cell('TOP_CELL')

w = Wafer(top, 'WAFER', 150000)
m = Mask(top, 'MASK', 7*25400, {
    "DATE": "2020-03-12",
    "USER": "jorich",
    "LAYOUT": "DIODE-RUN-1"
})

d15 = Diode(None, 'DIODE_15mm', 15000)
d12 = Diode(None, 'DIODE_12mm', 12000)
d8 = Diode(None, 'DIODE_8mm', 8000)
d5 = Diode(None, 'DIODE_5mm', 5000)
d2 = Diode(None, 'DIODE_2mm', 2000)

spacing = 1000

offset = spacing/2

ystart = [-52000, -53500, -50000, -45000, -41000]

for ii, d in enumerate([d15, d12, d8, d5, d2]):

    yspacing = d.height + spacing

    xstart = offset + d.width/2

    n = math.ceil(-2*ystart[ii] / yspacing)
    if ii <= 1:
        n -= 1

    top.add(gdspy.CellArray(d.cell, 1, n, (0, yspacing), origin=(xstart, ystart[ii])))
    top.add(gdspy.CellArray(d.cell, 1, n, (0, yspacing), origin=(-xstart, ystart[ii])))

    offset += d.width + spacing


lib.write_gds('BRNC_Run1_202003.gds')

gdspy.LayoutViewer(lib)
