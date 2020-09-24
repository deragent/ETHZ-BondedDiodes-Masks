import gdspy
import math

import numpy as np

## Disable the default lib to make multi lib use possible
gdspy.library.use_current_library = False

from mask import config as GC
from mask.processes import BRNC_202003
from mask.macros import Run1_TestSet

from mask.tools import MaskMerge

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine
from mask.elements import CallbackGenerator



def main(args):

    ### Create the library and top cell
    lib = gdspy.GdsLibrary()
    GC.GLOBAL["LIB"] = lib

    top = lib.new_cell('TOP_CELL')


    ### Create meta cells
    wafer = Wafer(top, 'WAFER', 150000)
    mask = Mask(top, 'MASK', 7*25400, {
            "DATE": "2020-03-12",
            "USER": "jorich",
            "LAYOUT": "DIODE-RUN-1%s"%("" if args.side is None else "-%s"%(args.side))
        }, githash=True)


    ### Add Markers
    markers, keepouts = BRNC_202003.createMarkers(lib)
    top.add(markers)



    ### Create diode cells
    diodes = lib.new_cell('DIODES')

    LABEL_HEIGHT = 300

    # if args.side is not None:
    #     LABEL = (args.side, LABEL_HEIGHT)
    # else:
    #     LABEL = None

    margin = 350
    dicingwidth = 100

    xoffset = margin

    ymin = [-61500, -61500, -56000, -49000, -42000, -36500]
    ymax = 50300

    DIODE_CONFIGS = [
        ['DIODE_15mm', 15000, 3000, 'A', 16300],
        ['DIODE_12mm', 12000, 3000, 'B', 13300],
        ['DIODE_8mm', 8000, 2000, 'C', 9300],
        ['DIODE_6mm', 6000, 2000, 'D', 7300],
        ['DIODE_4mm', 4000, 1000, 'E', 5300],
        ['DIODE_2mm', 2000, 1000, 'F', 3300],
    ]

    for ii, config in enumerate(DIODE_CONFIGS):

        x = xoffset + config[4]/2

        def createDiode(count, index):
            label = config[3] + str(count)
            name = config[0] + '_%i'%(count)
            window = config[2] if (index % 3) == 2 else 0

            element = Diode(None, name, config[1],
                            rounding=(config[1]/10), window=window,
                            label=(label, LABEL_HEIGHT))

            return element.cell

        generator = CallbackGenerator(createDiode)

        column_r = DeviceColumn(diodes, 'COLUMN_R_%s'%(config[0]), generator,
            x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

        generator.reset()

        column_l = DeviceColumn(diodes, 'COLUMN_L_%s'%(config[0]), generator,
            -1*x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=margin, dicingwidth=dicingwidth, keepout=keepouts)


        generator.addCellsToLib(lib)

        xoffset += config[4] + 2*margin

    top_dicing = DicingLine(GC.GLOBAL["LAYERS"]["DICING"], diodes,
        dicingwidth, (-48400, 50500), (48400, 50500))

    top.add(diodes)

    ## Add test structures (VPD + TLM)
    testset = Run1_TestSet(lib)

    top.add(gdspy.CellReference(testset, rotation=90, origin=(-63000, -5000)))
    top.add(gdspy.CellReference(testset, rotation=-90, origin=(+63000, +5000)))
    top.add(gdspy.CellReference(testset, rotation=0, origin=(-5000, +63000)))


    ### Save the gds file
    lib.write_gds(args.output)
    ### Save and svg representation
    top.write_svg(args.output + '.svg', 0.1)

    if args.export is not None:
        merge = MaskMerge(top)

        for name, layers in GC.GLOBAL["EXPORT"]:

            mask.setMaskName(name)

            merge.refresh()
            out = merge.mergeLayersIntoLib(layers, **GC.GLOBAL["LAYERS"][name])

            out.write_gds(args.export + "/%s.gds"%(name))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-1 [202003].')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of the output file.')
    parser.add_argument('-e', '--export', default=None,
                        help='Flag to export the fabrication mask layers into individual files.')
    parser.add_argument('-s', '--side', default=None, choices=["N", "P"],
                        help='Generate the mask for a specific side of the diodes.')

    args = parser.parse_args()

    main(args)
