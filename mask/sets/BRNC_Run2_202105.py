import gdspy
import math

import numpy as np

## Disable the default lib to make multi lib use possible
gdspy.library.use_current_library = False

from mask import config as GC
from mask.processes import BRNC_202105
from mask.macros import Run2_TestSet

from mask.tools import MaskMerge
from mask.tools import Outline

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine, Flood
from mask.elements import CallbackGenerator



def main(args):

    ### Create the library and top cell
    lib = gdspy.GdsLibrary()
    GC.GLOBAL["LIB"] = lib

    top = lib.new_cell('TOP_CELL')


    outline = Outline(100000, flat=32500)


    ### Create meta cells
    wafer = Wafer(top, 'WAFER', 100000, flat=32500, margin=3000)
    mask = Mask(top, 'MASK', 5*25400, {
            "DATE": "2021-05-31",
            "USER": "jorich",
            "LAYOUT": "DIODE-RUN-2%s"%("" if args.side is None else "-%s"%(args.side))
        }, textheight=1500, margin=3000, githash=True)


    ### Add Markers
    markers, keepouts = BRNC_202105.createMarkers(lib)
    top.add(markers)

    ### Add Wafer Markers
    wafer_markers = BRNC_202105.createWaferAlignment(lib)
    top.add(wafer_markers)


    if args.side != 'P':

        ### Create diode cells
        diodes = lib.new_cell('DIODES')

        LABEL_HEIGHT = 300

        ADD_LABEL = (args.side == 'N')

        margin = 150
        dicingwidth = 100

        xoffset = margin

        ymin = [-43000, -40000, -35000, -29500, -24000]
        ymax = 29000

        DIODE_CONFIGS = [
            ['DIODE_12mm', 12000, 3000, 'B'],
            ['DIODE_8mm', 8000, 2000, 'C'],
            ['DIODE_6mm', 6000, 2000, 'D'],
            ['DIODE_4mm', 4000, 1000, 'E'],
            ['DIODE_2mm', 2000, 1000, 'F'],
        ]

        TOP_DICING_Y = 29000

        for ii, config in enumerate(DIODE_CONFIGS):

            def createDiode(count, index):
                if ADD_LABEL:
                    label = (config[3] + str(count), LABEL_HEIGHT)
                else:
                    label = None

                name = config[0] + '_%i'%(count)
                window = config[2] if (index % 3) == 2 else 0

                element = Diode(None, name, config[1],
                                rounding=(config[1]/10), window=window,
                                label=label)

                return element.cell

            generator = CallbackGenerator(createDiode)


            x = xoffset + generator.width()/2

            dicinglines = [0]

            column_r = DeviceColumn(diodes, 'COLUMN_R_%s'%(config[0]), generator,
                x, ymin[ii], min(-1*ymin[ii], ymax),
                margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

            dicinglines.append(column_r.cell.get_bounding_box()[1][0])

            generator.reset()

            column_l = DeviceColumn(diodes, 'COLUMN_L_%s'%(config[0]), generator,
                -1*x, ymin[ii], min(-1*ymin[ii], ymax),
                margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

            dicinglines.append(column_l.cell.get_bounding_box()[0][0])


            generator.addCellsToLib(lib)


            # Add vertical dicing lines from the wafer edge
            for pos in dicinglines:
                ystart = outline.yMaxAtX(pos)
                if ystart > TOP_DICING_Y:
                    ystart = TOP_DICING_Y

                if pos != 0:
                    pos = pos - math.copysign(dicingwidth/2, pos)

                line = DicingLine(GC.GLOBAL["LAYERS"]["DICING"], diodes,
                    dicingwidth, (pos, ystart), (pos, outline.yMinAtX(pos)))


            xoffset += generator.width() + 2*margin

        # Horizontal dicing line to separate the top test structures
        top_dicing = DicingLine(GC.GLOBAL["LAYERS"]["DICING"], diodes,
            dicingwidth, (outline.xMinAtY(TOP_DICING_Y), TOP_DICING_Y), (outline.xMaxAtY(TOP_DICING_Y), TOP_DICING_Y))

        top.add(diodes)

    else:

        # Create the flood backside doping and metalization
        backside = lib.new_cell('BACKSIDE')

        for layer_name in ["CONTACT_DOPING", "METALIZATION"]:
            flood = Flood(
                GC.GLOBAL["LAYERS"][layer_name], backside,
                (-59000, -63000), (+59000, +50500),
                radius=90000/2 , keepout=keepouts
            )

        top.add(backside)

    ## Add test structures (VPD + TLM)
    testset_vert, testset_hor = Run2_TestSet(lib)

    top.add(gdspy.CellReference(testset_vert, rotation=180, origin=(+42500, -11000), x_reflection=True))
    top.add(gdspy.CellReference(testset_vert, rotation=0, origin=(-42500, -11000)))

    top.add(gdspy.CellReference(testset_hor, rotation=180, origin=(+32500, +31000), x_reflection=True))
    top.add(gdspy.CellReference(testset_hor, rotation=0, origin=(-32500, +31000)))


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

            ### Save and svg representation
            style = {(GC.GLOBAL["LAYERS"][name]["layer"], GC.GLOBAL["LAYERS"][name]["datatype"]): {'fill': '#FFFFFF'}}
            out.top_level()[0].write_svg(args.export + "/%s.svg"%(name), 0.02, style=style)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-2 [202105].')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of the output file.')
    parser.add_argument('-e', '--export', default=None,
                        help='Flag to export the fabrication mask layers into individual files.')
    parser.add_argument('-s', '--side', default=None, choices=["N", "P"],
                        help='Generate the mask for a specific side of the diodes.')

    args = parser.parse_args()

    main(args)