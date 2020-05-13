import gdspy

from ..elements.test import Resistance

def Run1_TestRes(lib, top):
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
